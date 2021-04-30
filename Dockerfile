FROM alpine
MAINTAINER Bryan Lim
RUN apk update
RUN apk add python3
RUN apk add py-pip
RUN pip install bs4
COPY get_company_fair_valuation.py /home/user/get_company_fair_valuation.py
WORKDIR /home/user
CMD ["python3","/home/user/get_company_fair_valuation.py"]