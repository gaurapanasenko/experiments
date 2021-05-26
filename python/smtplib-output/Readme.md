# Trying to catch status output while sending message with `smtplib`

It is very strange, but there is not way to save status output to varible while using smtplib. All output will be written to `stderr` stream. So the only way to get this output is overriding `stderr` stream with `os.dup2(x, 2)` or something similar.