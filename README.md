

#  Bike Store Dashboard

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

## Огляд проекту

Bike Store Dashboard — це веб-додаток для візуалізації та аналізу даних продажів мережі магазинів велосипедів. Проект реалізований за допомогою Streamlit із підключенням до бази даних MS SQL Server. Дашборд надає інтерактивний інтерфейс для аналізу ключових показників ефективності (KPI), тенденцій продажів та розподілу доходів за різними категоріями.

## Технічні характеристики

- **Фреймворк**: Streamlit
- **База даних**: MS SQL Server (Amazon RDS)
- **Бібліотеки візуалізації**: Plotly Express, Plotly Graph Objects, Matplotlib, Seaborn
- **Робота з даними**: Pandas, NumPy
- **Підключення до БД**: pymssql

## Архітектура додатку

Додаток складається з наступних функціональних компонентів:

1. **Підключення до бази даних**:
   - Функція `connect_to_db()` — встановлює з'єднання з базою даних MS SQL
   - Функція `fetch_data(query)` — виконує запити до бази даних та повертає результати у форматі Pandas DataFrame

2. **Інтерфейс користувача**:
   - Заголовок дашборду
   - Фільтри (рік, штат)
   - Секція з ключовими метриками
   - Візуалізації даних

3. **Візуалізації**:
   - Графік доходів за роками (стовпчикова діаграма)
   - Графік доходів за місяцями (лінійний графік)
   - Розподіл доходів за категоріями (treemap)
   - Розподіл доходів за магазинами (кругова діаграма)
   - Розподіл доходів за брендами (кругова діаграма)

## Функціональні можливості

### Фільтрація даних

Користувач може фільтрувати дані за наступними параметрами:
- **Рік**: вибір конкретного року з доступних в базі даних
- **Штат**: вибір конкретного штату або всіх штатів одразу

### Ключові метрики

Дашборд відображає наступні ключові показники:
- **Revenue**: загальний дохід за обраний період та регіон
- **Total Units**: загальна кількість проданих одиниць товару
- **# Units**: кількість унікальних товарів
- **# Customers**: кількість унікальних клієнтів

### Візуалізації

1. **Revenue by year**: стовпчикова діаграма, що показує динаміку доходів за роками
2. **Revenue by month**: лінійний графік, що відображає щомісячний дохід протягом обраного року
3. **Revenue by Categories**: treemap-діаграма, що демонструє розподіл доходів за категоріями товарів
4. **Revenue by Stores**: кругова діаграма з розподілом доходів між магазинами
5. **Revenue by Brands**: кругова діаграма з розподілом доходів між брендами

## Структура бази даних

Додаток використовує базу даних BikeStores з наступними основними таблицями:
- **sales.orders**: інформація про замовлення
- **sales.order_items**: деталі замовлень (товари, кількість, ціна)
- **sales.customers**: дані про клієнтів
- **sales.stores**: інформація про магазини
- **production.products**: інформація про товари
- **production.categories**: категорії товарів
- **production.brands**: бренди товарів

## Запити до бази даних

Додаток використовує різні SQL-запити для отримання даних, включаючи:

1. Запити для отримання унікальних значень для фільтрів:
   - Список років
   - Список штатів

2. Запити для обчислення ключових метрик:
   - Загальний дохід
   - Кількість проданих одиниць товару
   - Кількість унікальних товарів
   - Кількість унікальних клієнтів

3. Запити для візуалізацій:
   - Дохід за роками
   - Дохід за місяцями для обраного року
   - Дохід за категоріями товарів
   - Дохід за магазинами
   - Дохід за брендами

## Стилізація

Дашборд має кастомну стилізацію CSS:
- Великий виразний заголовок з фоном
- Стилізовані блоки для відображення метрик
- Послідовна кольорова схема для всіх візуалізацій

## Встановлення та запуск

1. Встановити необхідні бібліотеки Python:
   ```
   pip install streamlit pandas pymssql matplotlib plotly seaborn numpy
   ```

2. Запустити додаток:
   ```
   streamlit run dashboard.py
   ```

## Примітки щодо безпеки

Поточна реалізація містить дані для підключення безпосередньо у коді, що не є рекомендованою практикою для виробничих середовищ. У продакшені рекомендується використовувати змінні середовища або інші безпечні методи управління конфіденційними даними.

## Майбутні вдосконалення

1. Додати можливість експорту даних
2. Створити додаткові фільтри (бренд, категорія)
3. Реалізувати прогнозування продажів
4. Додати аналіз ефективності продажів за продавцями
5. Створити детальний перегляд для кожного магазину
