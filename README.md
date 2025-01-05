1. Устанавливам необходимые программы:
sudo apt install protobuf-compiler

2. Создаем и переходим в виртуальное окружение:
python3 -m venv myenv
source myenv/bin/activate

3. Устанавливаем необходимые змеиные пакеты:
pip install protobuf

4. Компилируем msg.proto (опционально т.к. файл msg_pb2.py, вероятнее всего уже создан)
protoc --python_out=. msg.proto
