FROM ubuntu:18.04
MAINTAINER Bryan Lim
RUN apt-get update
RUN apt-get install -y npm
RUN npm install python3
COPY get_company_fair_valuation.py /home/user/get_company_fair_valuation.py
WORKDIR /home/user
CMD ["python3","get_company_fair_valuation.py"]