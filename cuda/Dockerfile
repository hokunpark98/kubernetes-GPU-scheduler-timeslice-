FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu20.04
ENV APP_HOME=/home/
WORKDIR $APP_HOME
COPY mylib.cpp mylib.cpp
COPY matrix.cu matrix.cu
EXPOSE 8080
RUN apt-get update && apt-get install -y sudo
RUN chmod +w /etc/sudoers
RUN echo 'user ALL=(ALL) NOPASSWD:ALL' | tee -a /etc/sudoers
RUN chmod -w /etc/sudoers
RUN apt-get install stress
RUN g++ -I/usr/local/cuda/include -fPIC -shared -o /usr/libmylib.so /home/mylib.cpp -ldl -L/usr/local/cuda/lib64 -lcudart
RUN nvcc -o /home/matrix /home/matrix.cu -cudart shared


