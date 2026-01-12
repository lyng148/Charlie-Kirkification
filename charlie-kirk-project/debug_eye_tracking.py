import cv2
import mediapipe as mp
import time

# Initialize
face_mesh_landmarks = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
cam = cv2.VideoCapture(0)

print("=== CHARLIE KIRK DEBUG MODE ===")
print("This will show your iris ratio in real-time")
print("Try looking up, straight, and down to see the values")
print("Press ESC to exit\n")

while True:
    ret, frame = cam.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    height, width, depth = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    processed_image = face_mesh_landmarks.process(rgb_frame)
    face_landmark_points = processed_image.multi_face_landmarks

    if face_landmark_points:
        one_face_landmark_points = face_landmark_points[0].landmark

        # Eye landmarks
        left = [one_face_landmark_points[145], one_face_landmark_points[159]]
        right = [one_face_landmark_points[374], one_face_landmark_points[386]]

        # Draw circles
        for landmark_point in left:
            x = int(landmark_point.x * width)
            y = int(landmark_point.y * height)
            cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

        for landmark_point in right:
            x = int(landmark_point.x * width)
            y = int(landmark_point.y * height)
            cv2.circle(frame, (x, y), 3, (255, 255, 0), -1)

        # Iris
        l_iris = one_face_landmark_points[468]
        r_iris = one_face_landmark_points[473]

        # Draw iris
        cv2.circle(frame, (int(l_iris.x * width), int(l_iris.y * height)), 3, (255, 0, 0), -1)
        cv2.circle(frame, (int(r_iris.x * width), int(r_iris.y * height)), 3, (255, 0, 0), -1)

        # Calculate ratios
        l_ratio = (l_iris.y - left[1].y) / (left[0].y - left[1].y + 1e-6)
        r_ratio = (r_iris.y - right[1].y) / (right[0].y - right[1].y + 1e-6)

        # Display on frame
        status = "LOOKING DOWN!" if (l_ratio < 0.35 and r_ratio < 0.35) else "Normal"
        color = (0, 0, 255) if status == "LOOKING DOWN!" else (0, 255, 0)

        cv2.putText(frame, f"Left: {l_ratio:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.putText(frame, f"Right: {r_ratio:.2f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.putText(frame, status, (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # Print to console
        print(f"\rLeft: {l_ratio:.3f} | Right: {r_ratio:.3f} | {status}    ", end="", flush=True)

    cv2.imshow('Debug - Eye Tracking', frame)
    key = cv2.waitKey(100)

    if key == 27:  # ESC
        break

cam.release()
cv2.destroyAllWindows()
print("\n\nDebug session ended.")
