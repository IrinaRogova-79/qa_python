import pytest
from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_rating()) == 2

    # напиши свои тесты ниже
    @pytest.mark.parametrize("name", [
        "Книга",
        "A" * 40,  # Максимальная длина
        "Название с пробелами и знаками!",
        "1"
    ])
    def test_add_new_book_valid_names_success(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name in collector.get_books_genre()
        assert collector.get_book_genre(name) == ""

    @pytest.mark.parametrize("name", [
        "",  # Пустая строка
        "A" * 41,  # Слишком длинное название
    ])
    def test_add_new_book_invalid_names_not_added(self, name):
        collector = BooksCollector()
        initial_count = len(collector.get_books_genre())
        collector.add_new_book(name)
        assert len(collector.get_books_genre()) == initial_count
        if name:
            assert name not in collector.get_books_genre()

    def test_add_new_book_duplicate_name_not_added(self):
        collector = BooksCollector()
        collector.add_new_book("Уникальная книга")
        collector.add_new_book("Уникальная книга")
        assert len(collector.get_books_genre()) == 1
        assert collector.get_books_genre()["Уникальная книга"] == ""

    def test_set_book_genre_valid_genre_success(self):
        collector = BooksCollector()
        collector.add_new_book("Страшная книга")
        collector.set_book_genre("Страшная книга", "Ужасы")
        assert collector.get_book_genre("Страшная книга") == "Ужасы"

    def test_set_book_genre_invalid_genre_not_changed(self):
        collector = BooksCollector()
        collector.add_new_book("Странная книга")
        collector.set_book_genre("Странная книга", "Роман")
        assert collector.get_book_genre("Странная книга") == ""

    def test_set_book_genre_nonexistent_book_not_changed(self):
        collector = BooksCollector()
        collector.add_new_book("Существующая книга")
        collector.set_book_genre("Несуществующая книга", "Фантастика")
        assert collector.get_book_genre("Несуществующая книга") is None
        assert collector.get_book_genre("Существующая книга") == ""

    def test_get_book_genre_returns_correct_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Детектив")
        collector.set_book_genre("Детектив", "Детективы")
        assert collector.get_book_genre("Детектив") == "Детективы"

    def test_get_book_genre_returns_none_for_missing_book(self):
        collector = BooksCollector()
        assert collector.get_book_genre("Несуществующая") is None

    @pytest.mark.parametrize("genre", ["Фантастика", "Ужасы", "Детективы", "Мультфильмы", "Комедии"])
    def test_get_books_with_specific_genre_returns_correct_list(self, genre):
        collector = BooksCollector()
        book1 = f"Книга жанра {genre} 1"
        book2 = f"Книга жанра {genre} 2"
        collector.add_new_book(book1)
        collector.add_new_book(book2)
        collector.add_new_book("Другая книга")
        collector.set_book_genre(book1, genre)
        collector.set_book_genre(book2, genre)
        collector.set_book_genre("Другая книга", "Комедии")

        result = collector.get_books_with_specific_genre(genre)
        assert len(result) == 2
        assert book1 in result
        assert book2 in result
        assert "Другая книга" not in result

    def test_get_books_with_specific_genre_empty_if_no_books(self):
        collector = BooksCollector()
        assert collector.get_books_with_specific_genre("Фантастика") == []

    def test_get_books_genre_returns_dict(self):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга1", "Фантастика")

        result = collector.get_books_genre()
        assert isinstance(result, dict)
        assert result == {"Книга1": "Фантастика", "Книга2": ""}

    def test_get_books_for_children_excludes_age_rated_books(self):
        collector = BooksCollector()
        collector.add_new_book("Детская книга")
        collector.add_new_book("Страшная книга")
        collector.add_new_book("Детектив")

        collector.set_book_genre("Детская книга", "Мультфильмы")
        collector.set_book_genre("Страшная книга", "Ужасы")
        collector.set_book_genre("Детектив", "Детективы")

        result = collector.get_books_for_children()
        assert len(result) == 1
        assert "Детская книга" in result
        assert "Страшная книга" not in result
        assert "Детектив" not in result

    def test_get_books_for_children_excludes_books_without_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Книга без жанра")
        collector.add_new_book("Добрая книга")
        collector.set_book_genre("Добрая книга", "Комедии")

        result = collector.get_books_for_children()
        assert len(result) == 1
        assert "Добрая книга" in result
        assert "Книга без жанра" not in result

    def test_add_book_in_favorites_success(self):
        collector = BooksCollector()
        collector.add_new_book("Любимая книга")
        collector.add_book_in_favorites("Любимая книга")
        assert "Любимая книга" in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_duplicate_not_added(self):
        collector = BooksCollector()
        collector.add_new_book("Популярная книга")
        collector.add_book_in_favorites("Популярная книга")
        collector.add_book_in_favorites("Популярная книга")
        assert len(collector.get_list_of_favorites_books()) == 1

    def test_add_book_in_favorites_nonexistent_book_not_added(self):
        collector = BooksCollector()
        collector.add_book_in_favorites("Несуществующая книга")
        assert collector.get_list_of_favorites_books() == []

    def test_delete_book_from_favorites_success(self):
        collector = BooksCollector()
        collector.add_new_book("Книга для удаления")
        collector.add_book_in_favorites("Книга для удаления")
        assert len(collector.get_list_of_favorites_books()) == 1

        collector.delete_book_from_favorites("Книга для удаления")
        assert len(collector.get_list_of_favorites_books()) == 0
        assert "Книга для удаления" not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_nonexistent_book_no_error(self):
        collector = BooksCollector()
        collector.add_new_book("Существующая")
        collector.add_book_in_favorites("Существующая")
        initial_favorites = collector.get_list_of_favorites_books().copy()

        collector.delete_book_from_favorites("Несуществующая")
        assert collector.get_list_of_favorites_books() == initial_favorites

    def test_get_list_of_favorites_books_returns_list(self):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.add_book_in_favorites("Книга1")
        collector.add_book_in_favorites("Книга2")

        favorites = collector.get_list_of_favorites_books()
        assert isinstance(favorites, list)
        assert len(favorites) == 2
        assert "Книга1" in favorites
        assert "Книга2" in favorites

    def test_integration_add_and_set_and_favorite(self):
        """Интеграционный тест: добавление книги, установка жанра, добавление в избранное"""
        collector = BooksCollector()

        # Добавляем книгу
        collector.add_new_book("Гарри Поттер")
        assert collector.get_book_genre("Гарри Поттер") == ""

        # Устанавливаем жанр
        collector.set_book_genre("Гарри Поттер", "Фантастика")
        assert collector.get_book_genre("Гарри Поттер") == "Фантастика"

        # Добавляем в избранное
        collector.add_book_in_favorites("Гарри Поттер")
        assert "Гарри Поттер" in collector.get_list_of_favorites_books()

        # Проверяем, что книга есть в списке для детей (Фантастика не в age_rating)
        children_books = collector.get_books_for_children()
        assert "Гарри Поттер" in children_books

        # Удаляем из избранного
        collector.delete_book_from_favorites("Гарри Поттер")
        assert "Гарри Поттер" not in collector.get_list_of_favorites_books()
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()