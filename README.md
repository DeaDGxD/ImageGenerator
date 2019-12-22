### Postarałem się zrobić ten program, jak najbardziej uniwersalnym się tylko dało

### Można w nim dostosować sporo różnych opcji, takich jak:
 - maksymalna i minimalna wielkość czcionki (zmienia się zależnie od
   wielkości obrazu i najdłuższej linijki)
 - wymiary obrazu
 - kolory tła oraz obu czcionek


### Jak używać programu:
- Uruchomić program, aby móc ustawić config
    - Kiedy zostanie już stworzony plik config.ini, można go także modyfikować otwierając go np. notatnikiem
- W folderze teksty, utworzyć dowolną ilość plików tekstowych (.txt)
- Formatowanie tekstu:
	- Aby tekst wyświetlał się na kolor drugiej czcionki, użyj znaków `*` (gwiazdki) np: `*teraz jest na* inny *kolor* niż teraz`
	- Linijki będą wypisywane tak samo, jak w pliku .txt, no chyba, że jest za długa, to częśc słów przejdzie do następnej
	- **UWAGA** linijki nie przechodzą między następnymi obrazami, także nadmiar w jednym, zostanie ucięty
	- Wielkość czcionki jest zależna od długości, najdłuższej linijki tak, aby mogła się zmieścić w obrazie, jeżeli nadal będzie
		za długa, to część słów zostanie przesunięta na początek następnej
	- Aby część tekstu była zapisana już w następnym obrazie, to oddziel tą część znakiem % w jednej linijce od reszy
	- **UWAGA** prosiłbym nie dawać kilku spacji koło siebie, nie używać tab'u, oraz najlepiej nie dawać ich na początku oraz końcu linijki
- Uruchomić program ponownie, zdjęcia powinny zostać wygenerowane w folderze images
- Każdy tekst będzie miał przypisany do siebie folder o takiej samej nazwie jak plik tekstowy
- Przed następnym użyciem, proszę wyczyścić Folder Images
