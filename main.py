import flet as ft
import music

def main(page: ft.Page):
    
    #COLORS
    bgcolor = "#100017"
    primary = "#41005E"
    secondary = "#F1DEFA"
    
    #PAGE SETUP
    page.title = "Geet"
    page.horizontal_alignment = "center"
    page.bgcolor = bgcolor
    

    #ACTIONS
    music.createcache()


    def play(e):
        
        loadbar.width = 450
        page.update()

        #Release resources and clear cache
        song.release()
        music.resetcache()

        #Download via videoId and set the new song src
        music.dmusic(e.control.data[2])
        song.src = url + music.getaudio()
        
        #Update music player
        current_song.title = ft.Text(e.control.data[0], max_lines=2, overflow="ellipsis")
        current_song.subtitle = ft.Text(e.control.data[1])
        
        #Play the song
        song.play()

        #Update music player
        playpausebtn.icon = ft.icons.PAUSE_CIRCLE_ROUNDED
        music_player.disabled = False

        loadbar.width = 0

        page.update()


    def listsongs(e):

        if search_box.value != "":
            loadbar.width = 450
            page.update()
            
            songdict = music.searchsong(search_box.value)

            song_list.controls.clear()

            for song in songdict:
                
                song_item = ft.ListTile(width=450)
                song_item.title = ft.Text(song["title"], color=secondary)
                song_item.subtitle = ft.Text(song["artists"][0]["name"])
                song_item.data = [song["title"], song["artists"][0]["name"], song["videoId"]]
                song_item.on_click = play

                song_list.controls.append(song_item)

                page.update()

            print("Updated List")

            loadbar.width = 0
            page.update()


    def play_pause_song(e):

        if playpausebtn.icon == ft.icons.PLAY_CIRCLE_ROUNDED:
            
            playpausebtn.icon = ft.icons.PAUSE_CIRCLE_ROUNDED
            song.resume()

        elif playpausebtn.icon == ft.icons.PAUSE_CIRCLE_ROUNDED:

            playpausebtn.icon = ft.icons.PLAY_CIRCLE_ROUNDED
            song.pause()

        page.update()


    def repeat_song(e):

        if playpausebtn.icon == ft.icons.PLAY_CIRCLE_ROUNDED:
            
            playpausebtn.icon = ft.icons.PAUSE_CIRCLE_ROUNDED
            song.play()

        else:
            song.play()

        page.update()

    
    def checkstatus(e):

        if e.data == "completed":
            playpausebtn.icon = ft.icons.PLAY_CIRCLE_ROUNDED
            page.update()


    #UI COMPONENTS
    
    #Audio
    url = "../"
    song = ft.Audio(src=url+music.getaudio(), autoplay=False, on_state_changed=checkstatus)
    page.overlay.append(song)
    

    #App title
    app_name = ft.Text("geet", style=ft.TextThemeStyle.HEADLINE_LARGE, size=50, color=ft.colors.WHITE,
    weight="bold", italic=True)


    #Loading bar
    loadbar = ft.ProgressBar(width=0, color=secondary)
    

    #Song List
    song_list = ft.Column([], spacing=10, scroll="always", expand=True, horizontal_alignment="stretch")


    #Search Box
    search_box = ft.TextField(filled=True, border_width=2, border_radius=20, 
    hint_text="Enter a song name", width=450, prefix_icon=ft.icons.SEARCH_ROUNDED,
    on_submit=listsongs, focused_border_color=secondary, selection_color=secondary)


    #Music Player
    current_song = ft.ListTile(leading=ft.Icon(ft.icons.MUSIC_NOTE, size=40, color=secondary), title=ft.Text("..."),
    subtitle=ft.Text("..."), width=200)

    playpausebtn = ft.IconButton(icon=ft.icons.PLAY_CIRCLE_ROUNDED, icon_size=30, on_click=play_pause_song, icon_color=secondary)
    
    repeatbtn = ft.IconButton(icon=ft.icons.REPEAT_ROUNDED, icon_size=30, on_click=repeat_song, icon_color=secondary)

    player_button = ft.Row(
        [
            playpausebtn, repeatbtn
        ],
        alignment="end"
    )

    music_player = ft.Container(content=ft.Row(
            [
                current_song,
                player_button,
            ],
            alignment="spaceBetween"
        ), border_radius=20, disabled=True, bgcolor=primary, padding=ft.padding.only(right=10)
    )

    

    #LAYOUT  
    page.add(
        ft.Column(
            [
                app_name, search_box, loadbar, song_list,
            ],
            horizontal_alignment="center",
            spacing=20, expand=True
        ),
        music_player
    )


    
ft.app(target=main, assets_dir="cache", view=ft.WEB_BROWSER)