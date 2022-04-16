from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import time
import datetime

app = Client("my_account")

@app.on_message(filters.command("log", prefixes=".") & filters.me)
def log(_, msg):
	try:
		if msg.command[1] != 'this':
			orig_text = msg.command[1]
			if msg.command[1] == 'seek':
				for dialog in app.iter_dialogs():
					if dialog.chat.title == msg.command[2]:
						orig_text = dialog.chat.id
						fromChannel = True
						chattitle = dialog.chat.title
		elif msg.command[1] == 'this':
			fromChannel = False
			orig_text = msg.chat.id
		else:
			fromChannel = False
	except:
		fromChannel = False
		pass

	msg.edit_text(f"Производится сохранение логов чата по id: {orig_text}")
	try:
		tochkiKol = 0
		for message in app.iter_history(orig_text):
			log = open(f"logfile-{orig_text}.txt", "a", encoding="utf-8")
			messageTime = datetime.datetime.fromtimestamp(message.date)
			messagedater = datetime.datetime.fromtimestamp(message.date).date()
			if 'messagePreviousDate' not in locals():
				log.write(f"({messagedater})\n")
				messagePreviousDate = messageTime = datetime.datetime.fromtimestamp(message.date).date()
			elif messagePreviousDate != messageTime.date():
				log.write(f"({messagedater})\n")
				messagePreviousDate = messagedater
				pass
			tochki = "." * tochkiKol
			try:
				msg.edit_text(f"Производится сохранение логов чата по id: {orig_text}" + tochki)
			except:
				pass
			if tochkiKol == 3:
			    tochkiKol = 0
			else:
				tochkiKol += 1
			if message.text is not None:
					messagetimer = datetime.datetime.fromtimestamp(message.date).time()
					if fromChannel is not True:
						log.write(f"{message.from_user.first_name} ({messagetimer}): {message.text}\n")
					else:
						log.write(f"{chattitle} ({messagetimer}): {message.text}\n")
					try:
						if fromChannel is not True:
							app.download_media(message)
							log.write(f"{message.from_user.first_name} ({messagetimer}): <SENT MEDIA AND TEXT> {message.text}\n")
						else:
							app.download_media(message)
							log.write(f"{chattitle} ({messagetimer}): <SENT MEDIA AND TEXT> {message.text}\n")
					except:
						pass
			elif message.text is None:
				try:
					if fromChannel is not True:
						app.download_media(message)
						log.write(f"{message.from_user.first_name} ({messagetimer}): <SENT MEDIA>\n")
					else:
						app.download_media(message)
						log.write(f"{chattitle} ({messagetimer}): <SENT MEDIA>\n")

				except:
					pass
			log.close()
			time.sleep(0.1)
		msg.edit_text(f"Логи по id {orig_text} успешно сохранены!")

	except FloodWait as e:
		time.sleep(e.x)

app.run()