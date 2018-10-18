# VkBot

Ты сыч? Тебе скучно? Давно не кикали из конфы? Тогда эта прога для тебя, засри конфу НЕВЕРОЯТНО смешными мемами. Уже в предвкушении тогда поiхали:

## Установка

Для использования данного приложения необходим python 3й версии.

### Unix
```
python3 -m pip install -r packeges.txt
```
### Windows
```
python -m pip install -r packeges.txt
```
или
```
python.exe -m pip install -r packeges.txt
```
## Перед запуском
**Дорогой анонас, заполни info.json, в поле 'domain' ты можешь фставить свои смешнявые паблосы для мэмов,
 в 'chat_ids' ты можешь вставить id конф, в которые бот будет спамить, а также в 'messages' можешь вставить свои оригинатьные комментарии**

### Пример info.json

```
{
  "domain": ["picrandom", "memoirmem", "mudakoff", "degrook", "degroklassniki", "4ch"],
  "messages": ["ыыыы такая ржака", "хех от смеха жопу порвало", "рофл", "ахахахаххахах", "обоссаца"],
  "chat_ids": ["95"]
}
```

"posts" - ид постов<br/>
"messages" - ид сообщений(диалог/чат)<br/>

**Ид чата**
![Alt text](https://i.imgur.com/WqnELpG.png "Ид чата")<br/>

## Запуск

### Unix
```
python3 ./src/bot2.0.py
```
### Windows
```
python ./src/bot2.0.py
```
или
```
python.exe ./src/bot2.0.py
```