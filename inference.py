import sys
import os
from ultralytics import YOLO

MODEL_PATH = './weights/best.pt'

def main():
    if len(sys.argv) < 2:
        print("Usage: python inference.py <path_to_file>")
        return
    dataset_path = sys.argv[1]

    model = YOLO(MODEL_PATH)

    print('Running inference...\n')

    results = model(dataset_path, verbose=False)

    def get_id_from_path(path):
        return os.path.splitext(os.path.basename(path))[0]

    with open('submission.csv', 'w') as file:
        file.write("patientId,PredictionString\n")
        for result in results:
            line = get_id_from_path(result.path) + ','
            
            for conf, xywh in zip(result.boxes.conf, result.boxes.xywh):
                x, y, w, h = xywh
                line += f"{conf:.2f} {x:.2f} {y:.2f} {w:.2f} {h:.2f} "
                
            line = line.strip()
            file.write(line+"\n")

if __name__ == "__main__":
    main()