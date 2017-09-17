# Face detector notifier

A system that sends an email with an image attached if a face appears on camera.

# How to run

`python face_detector.py`

A stream of the camera will appear. When a face be detected, it will send and email in background.

Change the variable `frequency` in `face_detector.py` to the minimal amount of minutes you want between each email.

And change the variables `fromaddr`, `password` and `toaddr` in `email_sender.py`, where `fromaddr` is an valid Gmail which you are able to loging using the value you set for `password`. The variable `toaddr` is the recipient you will send the email.

### Attention

DO NOT set the `frequenty` to zero or remove any limitations on that. It will cause the software to send an email for each frame where a face was detected. It could be a lot of e-mails and sending to much emails at once certantly is not a good idea.

### Author

**Maikel Maciel Rönnau**  
*Computer Scientist  
maikel.ronnau@ulbra.edu.br  
[Linkedin](https://br.linkedin.com/in/maikelronnau)*
