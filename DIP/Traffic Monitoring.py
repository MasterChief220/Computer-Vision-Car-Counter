
import cv2
vehiclexml=cv2.CascadeClassifier('vehicle.xml')

def detection(frame, vehicle_count, vehicle_ids):
    vehicle = vehiclexml.detectMultiScale(frame, 1.15, 4)
    for (x, y, w, h) in vehicle:
        # Check if the vehicle is on the desired side of the screen
        if x < frame.shape[1] / 2:
            # Check if the vehicle has already been counted
            vehicle_id = f'{x}-{y}-{w}-{h}'
            if vehicle_id not in vehicle_ids:
                # Check if the vehicle has moved a certain distance from its previous location
                min_distance = float('inf')
                for prev_vehicle_id in vehicle_ids:
                    prev_x, prev_y, prev_w, prev_h = map(int, prev_vehicle_id.split('-'))
                    distance = ((prev_x - x) ** 2 + (prev_y - y) ** 2) ** 0.5
                    min_distance = min(min_distance, distance)
                if min_distance > 20:
                    vehicle_count += 1
                    vehicle_ids.add(vehicle_id)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
                    cv2.putText(frame, 'vehicle detected.!', (x + w, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), thickness=2)
    cv2.putText(frame, f'Vehicle count: {vehicle_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), thickness=2)
    return frame, vehicle_count

def capturescreen():
    realtimevideo = cv2.VideoCapture('video.avi')
    vehicle_count = 0
    vehicle_ids = set()
    while realtimevideo.isOpened():
        ret, frame = realtimevideo.read()
        controlkey = cv2.waitKey(1)
        if ret:
            vehicleframe, vehicle_count = detection(frame, vehicle_count, vehicle_ids)
            cv2.imshow('vehicle detection', vehicleframe)
        else:
            break
        if controlkey == ord('q'):
            break

    realtimevideo.release()
    cv2.destroyAllWindows()

capturescreen()

