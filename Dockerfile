FROM alpine
MAINTAINER Bryan Lim
RUN apk update
RUN apk install python3
COPY get_company_fair_valuation.py /home/user/get_company_fair_valuation.py
WORKDIR /home/user
CMD ["python3","/home/user/get_company_fair_valuation.py"]