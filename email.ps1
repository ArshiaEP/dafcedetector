$fromaddress = “emailaddress”
$toaddress = "emailaddress"
$Subject = “Dafece Notification”
$body = "Deface error!please check attached pictures"
$attachment1 = $args[0]
$attachment2 = $args[1]
$smtpserver = “mailserver addrsss”
##################################
$message = new-object System.Net.Mail.MailMessage
$message.From = $fromaddress
$message.To.Add($toaddress)
$message.Subject = $Subject
#$message.CC.Add("")
$message.CC.Add("emailaddress")
$message.CC.Add("emailaddress")
$message.CC.Add("emailaddress")
$message.CC.Add("emailaddress")
$attach = new-object Net.Mail.Attachment($attachment1)
$attach1 = new-object Net.Mail.Attachment($attachment2)
$message.Attachments.Add($attach)
$message.Attachments.Add($attach1)
$message.body = $body
$smtp = new-object Net.Mail.SmtpClient($smtpserver)
$smtp.Send($message)
