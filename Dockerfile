# selected image. I think that in ubuntão it could be more agile, then I will carry out a test..
FROM python:3.11


# changing build directory
WORKDIR /app


# copy dependency on root
COPY requirements.txt ./
RUN pip install -r requirements.txt


#  other layer init 
COPY . /app
RUN make init
CMD make execute 


EXPOSE 8000
