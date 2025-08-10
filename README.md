# Points to consider
1. Refer to [this pdf](DA5402_MLOPS_A2.pdf) for the problem statement.
2. A DockerFile with requirements.txt is provided. Please use that to build images in case of library unavailability or version mismatch.
3. In contrast to assignment-1, Selenium is discarded upon realization that the images in GNews are API attachments and can all be retrieved using page source from Requests.
4. For the mail configuration, please add the following environment variables in docker compose
   - AIRFLOW__SMTP__SMTP_HOST: smtp.gmail.com
   - AIRFLOW__SMTP__SMTP_STARTTLS: True
   - AIRFLOW__SMTP__SMTP_SSL: False
   - AIRFLOW__SMTP__SMTP_USER:  #your mail id
   - AIRFLOW__SMTP__SMTP_PASSWORD: #your app password
   - AIRFLOW__SMTP__SMTP_PORT: 587
   - AIRFLOW__SMTP__SMTP_MAIL_FROM: #your name and mail
5. Please add a Postgres and File connection in the Docker UI
