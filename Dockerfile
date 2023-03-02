RUN apt update && apt upgrade 
RUN git clone https://github.com/desinobita/AutoAnimeBot
RUN pip3 install -U -r requirements.txt 

CMD python3 ak4sh.py
