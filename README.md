<h1 align="center"> Schedule Telegram Bot </h1>

<div align="center">
    <img src="https://badges.frapsoft.com/os/v1/open-source.svg?v=103">
    <h3>This telegram bot was created for user-friendly experience with the schedule of classes at the university.</h3>
</div>

## ✅| Futures
- Easily edit your schedule with Django admin.
- Schedule for even and odd weeks.
- Sending the current day's schedule and a short schedule for the next day.
- User menu with option to change group and enable/disable notifications.
- Admin menu with mass mailing feature.
- Logging system.
- Ability to use static Django files with DEBUG=False.
- Fully asynchronous.

## 📦| Install
- Install python and git.
```shell
    apt install -y git python3 postgresql postgresql-contrib
```
- Clone this git repository.
```shell
    git clone https://github.com/nisemup/Schedule-Telegram-Bot/
```
- Install requirements with pip3
```shell
    pip3 install -r requirements.txt
```

## 📝| Configuration

**Configuring PostgreSQL:**
- Switching to a postgres account on your server. (default password - postgres) 
```shell
    sudo -u postgres psql
```
- Create user and database.
```shell
    create database schedule;
    create user admin with encrypted password 'password';
    grant all privileges on database schedule to admin;
```

⚠️⚠️ [Do not forget to configure remote connection permissions for PostgreSQL](https://www.bigbinary.com/blog/configure-postgresql-to-allow-remote-connection) ⚠️⚠️

**Change** /settings/.env.template **to** /settings/.env

**Configuring** /settings/.env:
- `BOT_API_TOKEN` - You can get it from [BotFather](https://t.me/botfather).
- `IPv4` - IPv4 address of the machine that hosts the bot.
- `DJANGO_KEY` - Django secret key.
- `DEBUG` - Django debug mode. (True/False)
- `MAIN_ADMIN` - Telegram ID of main admin. You can get it from [Userinfobot](https://t.me/userinfobot).
- `DB_HOST` - Database host (use 127.0.0.1)
- `DB_PORT` - Database port (default - 5432)
- `DB_NAME` - Database name (in our example - schedule)
- `DB_USER` - Database username (in our example - admin)
- `DB_PASSWORD` - Database password (in our example - password)

## ⚙️| Deployment
- Create a migration file and apply it.
```shell
   python3 manage.py makemigrations
   python3 manage.py migrate
```
- Collect static files.
```shell
    python3 manage.py collectstatic
```
- Start the bot.
```shell
    python3 app.py
```
