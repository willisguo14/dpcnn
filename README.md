# dpcnn

1. `SARD_xml.py` - get good and bad versions of mixed SARD files. (output included `SARD_mixed.zip`)
2. get ast using joern (ouput included in `ast.zip`) 
3. `data_preprocess.py` - tokenize ast. (output will be `data.npz`) 
4. `model.py` - train DP-CNN model

docker: `docker pull willisguo/dp-cnn:finished`
- implementation in `/root/DP-CNN`
