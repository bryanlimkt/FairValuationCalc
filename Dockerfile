FROM ubuntu:18.04
MAINTAINER Bryan Lim
RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN pip3 install bs4
RUN pip3 install lxml
RUN pip3 install requests
COPY get_company_fair_valuation.py /home/user/get_company_fair_valuation.py
WORKDIR /home/user
CMD ["python3","/home/user/get_company_fair_valuation.py"]