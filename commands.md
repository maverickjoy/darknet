TRAINING
========

1) Normal training
 >>> ./darknet detector train cfg/tic-obj.data cfg/tic-train-yolov3.cfg darknet53.conv.74

2) If training stopped in between use backup weights to resume training.
 >>> ./darknet detector train cfg/tic-obj.data cfg/tic-train-yolov3.cfg backup/tic-yolov3.backup

TESTING
=======

2) Testing
 >>> ./darknet detector test cfg/tic-obj.data cfg/tic-test-yolov3.cfg backup/tic-yolov3_final.weights
