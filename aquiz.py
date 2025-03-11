import streamlit as st
import os
import random, time
from PIL import Image

#funkcja do wczytywania obrazów z folderów
def load_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  #obsługuje obrazy w formatach PNG, JPG, JPEG
            img_path = os.path.join(folder_path, filename)
            images.append(img_path)
    return images

def app():

    if "cnt" not in st.session_state:
        st.session_state.cnt = 0

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "start" not in st.session_state:
        st.session_state.start = time.time()

    axel_folder = 'axel_res'  
    sd15_folder = 'aixel'  

    #wczytanie obrazów
    axel_images = load_images_from_folder(axel_folder)
    sd15_images = load_images_from_folder(sd15_folder)


    if "img_width" not in st.session_state:
        st.session_state.img_width = st.select_slider("Wybierz szerokość obrazków", options=[100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300], value=300)
    #sprawdzamy, czy reset został ustawiony i inicjujemy go, jeśli nie
    if "reset" not in st.session_state:
        st.session_state.reset = False

    #sprawdzamy, czy obrazki zostały już wylosowane (jeśli nie, to je losujemy)
    if "images" not in st.session_state or st.session_state.reset:
        axel_sample = random.sample(axel_images, 1)
        sd15_sample = random.sample(sd15_images, 4)

        #połączenie obrazów z obu folderów i losowanie kolejności

        correct_index = random.randint(0, 3)

        #zapisujemy w session_state

        full_ai =random.randint(0,4)
        if full_ai != 2:
            sd15_sample[correct_index] =  axel_sample[0]

        st.session_state.images = sd15_sample
        st.session_state.correct_answers = correct_index+1 if full_ai != 2 else 'Tu nie ma prawdziwego Axelka'
        st.session_state.user_answers = []
        st.session_state.reset = False

    #wyświetlanie obrazków w Streamlit w układzie 2x2
    st.title("Axel czy AIxel?")

    #wyświetlamy 4 obrazki w układzie 2x2
    cols = st.columns(2)
    for i, img_path in enumerate(st.session_state.images):
        img = Image.open(img_path)
        cols[i % 2].image(img, caption=f"Obrazek {i + 1}", width=st.session_state.img_width)

    #odpowiedzi użytkownika

    answer = st.radio('Które zdjęcia przedstawia prawdziwego Axelka?',('Tu nie ma prawdziwego Axelka',1,2,3,4))
    #przycisk do sprawdzenia wyniku
    if st.button("Sprawdź wynik"):

        if st.session_state.correct_answers == answer:
            st.success("Gratulacje! Poprawny wynik")
            st.session_state.score +=1
            st.session_state.cnt +=1
        else:
            st.error(f"Niestety, źle. Poprawna odpowiedz to {st.session_state.correct_answers}")
            st.session_state.cnt +=1
        st.write(f"Twój wynik to {st.session_state.score}/{st.session_state.cnt} (quiz składa się z 12 pytań)")

    #przycisk do ponownego losowania obrazków
    if st.session_state.cnt < 12:
        if st.button("Ponownie losuj obrazki"):
            st.session_state.reset = True
            st.rerun()
    else:
        elapsed_time = time.time() - st.session_state.start
        formatted_time = "{:02}:{:02}".format(int(elapsed_time // 60), int(elapsed_time % 60))

        st.write(f"To już koniec naszej zabawy. Twój wynik to {st.session_state.score}/{st.session_state.cnt} uzyskany w czasie {formatted_time} ")

if __name__ == "__main__":
    app()