import pytest
from main import BooksCollector


class TestBooksCollector:

    # Тесты для add_new_book
    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book("Гордость и предубеждение и зомби")
        collector.add_new_book("Что делать, если ваш кот хочет вас убить")
        assert len(collector.get_books_genre()) == 2

    @pytest.mark.parametrize("name", [
        "Книга",
        "A" * 40,
        "Название с пробелами и знаками!",
        "1"
    ])
    def test_add_new_book_valid_name_added_to_books_genre(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name in collector.get_books_genre()

    @pytest.mark.parametrize("name", [
        "Книга",
        "A" * 40,
        "Название с пробелами и знаками!",
        "1"
    ])
    def test_add_new_book_valid_name_has_empty_genre(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert collector.get_book_genre(name) == ""

    def test_add_new_book_empty_name_not_added(self):
        collector = BooksCollector()
        initial_count = len(collector.get_books_genre())
        collector.add_new_book("")
        assert len(collector.get_books_genre()) == initial_count

    def test_add_new_book_name_too_long_not_added(self):
        collector = BooksCollector()
        initial_count = len(collector.get_books_genre())
        collector.add_new_book("A" * 41)
        assert len(collector.get_books_genre()) == initial_count

    def test_add_new_book_duplicate_name_not_increased(self):
        collector = BooksCollector()
        collector.add_new_book("Уникальная книга")
        collector.add_new_book("Уникальная книга")
        assert len(collector.get_books_genre()) == 1

    def test_add_new_book_duplicate_name_keeps_first_entry(self):
        collector = BooksCollector()
        collector.add_new_book("Уникальная книга")
        collector.add_new_book("Уникальная книга")
        assert collector.get_books_genre()["Уникальная книга"] == ""

    # Тесты для set_book_genre
    def test_set_book_genre_valid_genre_set_successfully(self):
        collector = BooksCollector()
        collector.add_new_book("Страшная книга")
        collector.set_book_genre("Страшная книга", "Ужасы")
        assert collector.get_book_genre("Страшная книга") == "Ужасы"

    def test_set_book_genre_invalid_genre_not_set(self):
        collector = BooksCollector()
        collector.add_new_book("Странная книга")
        collector.set_book_genre("Странная книга", "Роман")
        assert collector.get_book_genre("Странная книга") == ""

    def test_set_book_genre_nonexistent_book_nothing_changes(self):
        collector = BooksCollector()
        collector.add_new_book("Существующая книга")
        collector.set_book_genre("Несуществующая книга", "Фантастика")
        assert collector.get_book_genre("Несуществующая книга") is None

    def test_set_book_genre_nonexistent_book_does_not_affect_existing(self):
        collector = BooksCollector()
        collector.add_new_book("Существующая книга")
        collector.set_book_genre("Несуществующая книга", "Фантастика")
        assert collector.get_book_genre("Существующая книга") == ""

    # Тесты для get_book_genre
    def test_get_book_genre_returns_correct_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Детектив")
        collector.set_book_genre("Детектив", "Детективы")
        assert collector.get_book_genre("Детектив") == "Детективы"

    def test_get_book_genre_returns_none_for_missing_book(self):
        collector = BooksCollector()
        assert collector.get_book_genre("Несуществующая") is None

    def test_get_book_genre_returns_empty_string_for_book_without_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Книга без жанра")
        assert collector.get_book_genre("Книга без жанра") == ""

    # Тесты для get_books_with_specific_genre
    @pytest.mark.parametrize("genre", ["Фантастика", "Ужасы", "Детективы", "Мультфильмы", "Комедии"])
    def test_get_books_with_specific_genre_returns_correct_count(self, genre):
        collector = BooksCollector()
        book1 = f"Книга жанра {genre} 1"
        book2 = f"Книга жанра {genre} 2"
        collector.add_new_book(book1)
        collector.add_new_book(book2)
        collector.set_book_genre(book1, genre)
        collector.set_book_genre(book2, genre)

        result = collector.get_books_with_specific_genre(genre)
        assert len(result) == 2

    @pytest.mark.parametrize("genre", ["Фантастика", "Ужасы", "Детективы", "Мультфильмы", "Комедии"])
    def test_get_books_with_specific_genre_returns_correct_books(self, genre):
        collector = BooksCollector()
        book1 = f"Книга жанра {genre} 1"
        book2 = f"Книга жанра {genre} 2"
        collector.add_new_book(book1)
        collector.add_new_book(book2)
        collector.set_book_genre(book1, genre)
        collector.set_book_genre(book2, genre)

        result = collector.get_books_with_specific_genre(genre)
        assert book1 in result
        assert book2 in result

    def test_get_books_with_specific_genre_does_not_return_other_genres(self):
        collector = BooksCollector()
        collector.add_new_book("Детектив")
        collector.add_new_book("Фантастика")
        collector.set_book_genre("Детектив", "Детективы")
        collector.set_book_genre("Фантастика", "Фантастика")

        result = collector.get_books_with_specific_genre("Детективы")
        assert "Фантастика" not in result

    def test_get_books_with_specific_genre_empty_if_no_books(self):
        collector = BooksCollector()
        assert collector.get_books_with_specific_genre("Фантастика") == []

    # Тесты для get_books_genre
    def test_get_books_genre_returns_dict(self):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        result = collector.get_books_genre()
        assert isinstance(result, dict)

    def test_get_books_genre_contains_all_added_books(self):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        result = collector.get_books_genre()
        assert "Книга1" in result
        assert "Книга2" in result

    def test_get_books_genre_shows_correct_genres(self):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.set_book_genre("Книга1", "Фантастика")
        result = collector.get_books_genre()
        assert result["Книга1"] == "Фантастика"

    # Тесты для get_books_for_children
    def test_get_books_for_children_excludes_age_rated_books(self):
        collector = BooksCollector()
        collector.add_new_book("Страшная книга")
        collector.set_book_genre("Страшная книга", "Ужасы")
        result = collector.get_books_for_children()
        assert "Страшная книга" not in result

    def test_get_books_for_children_includes_non_age_rated_books(self):
        collector = BooksCollector()
        collector.add_new_book("Детская книга")
        collector.set_book_genre("Детская книга", "Мультфильмы")
        result = collector.get_books_for_children()
        assert "Детская книга" in result

    def test_get_books_for_children_excludes_books_without_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Книга без жанра")
        result = collector.get_books_for_children()
        assert "Книга без жанра" not in result

    # Тесты для add_book_in_favorites
    def test_add_book_in_favorites_adds_book(self):
        collector = BooksCollector()
        collector.add_new_book("Любимая книга")
        collector.add_book_in_favorites("Любимая книга")
        assert "Любимая книга" in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_duplicate_not_increases_list(self):
        collector = BooksCollector()
        collector.add_new_book("Популярная книга")
        collector.add_book_in_favorites("Популярная книга")
        collector.add_book_in_favorites("Популярная книга")
        assert len(collector.get_list_of_favorites_books()) == 1

    def test_add_book_in_favorites_nonexistent_book_not_added(self):
        collector = BooksCollector()
        collector.add_book_in_favorites("Несуществующая книга")
        assert collector.get_list_of_favorites_books() == []

    # Тесты для delete_book_from_favorites
    def test_delete_book_from_favorites_removes_book(self):
        collector = BooksCollector()
        collector.add_new_book("Книга для удаления")
        collector.add_book_in_favorites("Книга для удаления")
        collector.delete_book_from_favorites("Книга для удаления")
        assert "Книга для удаления" not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_decreases_list_length(self):
        collector = BooksCollector()
        collector.add_new_book("Книга для удаления")
        collector.add_book_in_favorites("Книга для удаления")
        initial_length = len(collector.get_list_of_favorites_books())
        collector.delete_book_from_favorites("Книга для удаления")
        assert len(collector.get_list_of_favorites_books()) == initial_length - 1

    def test_delete_book_from_favorites_nonexistent_book_no_error(self):
        collector = BooksCollector()
        collector.add_new_book("Существующая")
        collector.add_book_in_favorites("Существующая")
        collector.delete_book_from_favorites("Несуществующая")
        assert len(collector.get_list_of_favorites_books()) == 1

    # Тесты для get_list_of_favorites_books
    def test_get_list_of_favorites_books_returns_list(self):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_book_in_favorites("Книга1")
        favorites = collector.get_list_of_favorites_books()
        assert isinstance(favorites, list)

    def test_get_list_of_favorites_books_contains_added_favorites(self):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.add_book_in_favorites("Книга1")
        collector.add_book_in_favorites("Книга2")
        favorites = collector.get_list_of_favorites_books()
        assert "Книга1" in favorites
        assert "Книга2" in favorites

    def test_get_list_of_favorites_books_empty_initially(self):
        collector = BooksCollector()
        assert collector.get_list_of_favorites_books() == []
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()