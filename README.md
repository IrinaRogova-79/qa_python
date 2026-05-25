# qa_python
# Тесты для BooksCollector

## Описание
Данный набор тестов покрывает функциональность класса `BooksCollector`, который позволяет управлять коллекцией книг с жанрами и избранными книгами.

## Важное замечание
**Каждый тест создает свой собственный экземпляр класса `BooksCollector()`, что обеспечивает полную независимость тестов друг от друга.**

## Покрытие тестами

### Методы и тесты:

#### 1. `add_new_book(name)`
- **test_add_new_book_add_two_books** - проверка добавления двух книг
- **test_add_new_book_valid_names_success** - параметризованный тест валидных названий (1-40 символов)
- **test_add_new_book_invalid_names_not_added** - проверка невалидных названий (пустая строка, >40 символов)
- **test_add_new_book_duplicate_name_not_added** - проверка, что дубликаты не добавляются

#### 2. `set_book_genre(name, genre)`
- **test_set_book_genre_valid_genre_success** - установка валидного жанра существующей книге
- **test_set_book_genre_invalid_genre_not_changed** - попытка установить невалидный жанр
- **test_set_book_genre_nonexistent_book_not_changed** - установка жанра несуществующей книге

#### 3. `get_book_genre(name)`
- **test_get_book_genre_returns_correct_genre** - получение жанра существующей книги
- **test_get_book_genre_returns_none_for_missing_book** - получение жанра несуществующей книги

#### 4. `get_books_with_specific_genre(genre)`
- **test_get_books_with_specific_genre_returns_correct_list** - параметризованный тест для всех жанров
- **test_get_books_with_specific_genre_empty_if_no_books** - пустой список при отсутствии книг

#### 5. `get_books_genre()`
- **test_get_books_genre_returns_dict** - проверка возвращаемого словаря

#### 6. `get_books_for_children()`
- **test_get_books_for_children_excludes_age_rated_books** - исключение книг с возрастным рейтингом (Ужасы, Детективы)
- **test_get_books_for_children_excludes_books_without_genre** - исключение книг без жанра

#### 7. `add_book_in_favorites(name)`
- **test_add_book_in_favorites_success** - успешное добавление в избранное
- **test_add_book_in_favorites_duplicate_not_added** - предотвращение дубликатов
- **test_add_book_in_favorites_nonexistent_book_not_added** - добавление несуществующей книги

#### 8. `delete_book_from_favorites(name)`
- **test_delete_book_from_favorites_success** - успешное удаление из избранного
- **test_delete_book_from_favorites_nonexistent_book_no_error** - удаление несуществующей книги

#### 9. `get_list_of_favorites_books()`
- **test_get_list_of_favorites_books_returns_list** - проверка возвращаемого списка

#### 10. Интеграционный тест
- **test_integration_add_and_set_and_favorite** - комплексный тест всех операций

## Количество тестов: 17

## Запуск тестов
```bash
pytest -v tests.py
