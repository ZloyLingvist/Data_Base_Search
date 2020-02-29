# Поиск математических утверждений в базе данных.

Программа, которая осуществляла бы такой поиск в некоторой базе данных.Предполагается, что как заданная теорема, так и теоремы 
из базы данных записаны на естественном языке (возможно, с использованием математических формул, представленных в формате системы tex). При этом в программе должно
учитываться, что формулировки заданной теоремы и той же теоремы в базе данных могут несколько отличаться. 
В любом случае, формулировка этой теоремы из базы данных должна появиться среди лучших кандидатов, найденных программой.

## Начало работы

Запустить gui_main.py. В появившемся окне в выпадающем списке выбрать формат данных, с которыми предстоит работать. 
На данном этапе доступны:
1. Использование уже разобранных предложения в conllu-формате (для их создания использовался синтаксический анализатор Abbyy Compreno -- Теорема в формате Abbyy)
2. Преобразование непосредственно введенной теоремы в поле Теорема (используется встроенный синтаксический анализатор Stamford nlp Parser -- Теорема в формате Stamford)
3. Подача в программу непосредственно разобранного дерева (список списков -- Разобранное дерево)
4. Для того, чтобы работать с формулой в формате tex в меню выбрать пункт Режимы - Работа с формулами.

#### Описание интерфейса

###### Кнопки
1. Ранжирование разборов. Автоматически разбирает введенную теорему (либо из файла, либо из поля для ввода)
2. Сделать разбор. Представление теоремы из файла или введенной теоремы в виде формулы.
3. Очистка. Очищает основное текстовое поле программы
4. Показать дерево. Строит по формуле дерево и выводит его на экран.
5. Установка библиотек.
6. Редактировать config-файл. Имена, пути всех необходимых для работы программы файлов занесены в файл конфигурации. После изменения нужно нажаь кнопку Сохранить

###### Меню
1. Параметры разбора.
1.1. Показать дерево при помощи ОС.
1.2. Синтаксическое дерево/Формула логики предикатов (0/1). В зависимости от включенного параметра формула останется в виде списка списков синтаксического представления или дополнительно будет преобразована к виду формулы логики предикатов.
2. Режимы
2.1 Работа с формулами. При нажатии будет открыто новое окно для работы непосредственно с формулами на языке tex
2.2 Режим разработчика. Открытие нового окна, в котором можно создавать базы данных для программы.
3. Выход - завершение работы программы

### Установка необходимых компонентов
Недостающие компоненты можно установить нажатием кнопки Установка библиотек.
В программе используются следующие компоненты.
1. Для преобразования формул на языке TeX библиотека TatSu. https://github.com/neogeny/TatSu Документация https://tatsu.readthedocs.io/en/stable/intro.html
2. Для визуализации деревьев используется пакет GraphViz. https://graphviz.gitlab.io/download/ Папку bin необходимо положить в корневую папку проекта.
3. 

### Краткое описание проекта

Предварительно исходные утверждения разделяются на текстовые утверждения и содержащиеся в них математические формулы. 
Формулы добавлялись в отдельный текстовый файл, а в самих теоремах заменяются на специальные обозначения. 

К каждому преобразованному таким образом утверждению применяется система ABBYY Compreno (в дальнейшем планируется использовать любой парсер русского языка), которая создает синтаксическое дерево для каждого предложения. Затем программа, написанная на языке Python 3, осуществляет перевод 
синтаксического представления теорем в формулу логики предикатов. На данном этапе произвольная теорема не может
быть представлена в таком виде, поэтому работа по улучшению данной части системы будет продолжаться. 

Для преобразования математических формул в форму необходимую,для дальнейшей работы, использовалась РБНФ-грамматика 
(расширенная форма Бэкуса—Наура) и библиотека для Python TatSu, которая позволяет по файлу с правилами построить дерево формулы. 

На следующем этапе работы специальные обозначения, введенные ранее в формулах логики предикатов, заменяются на деревья соответствующих формул. 
Полученная формула логики предикатов вносится в базу данных. Для удобства использования написан графический интерфейс.

### Используемые библиотеки

1. [TatSu](https://github.com/neogeny/TatSu)