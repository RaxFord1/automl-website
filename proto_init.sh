#conda init

pip install --upgrade protobuf

conda install -c anaconda protobuf

#conda activate training-ml
python -c "import google.protobuf; print(google.protobuf.__version__)"

whereis protoc

protoc --python_out=./ ./model_search/proto/phoenix_spec.proto
protoc --python_out=./ ./model_search/proto/hparam.proto
protoc --python_out=./ ./model_search/proto/distillation_spec.proto
protoc --python_out=./ ./model_search/proto/ensembling_spec.proto
protoc --python_out=./ ./model_search/proto/transfer_learning_spec.proto

echo "Finished protoc"

ls ./model_search/proto/

echo "CONDA PREFIX:"
echo $CONDA_PREFIX

python train.py
