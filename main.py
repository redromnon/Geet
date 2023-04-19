import flet as ft
import music, tempfile

def main(page: ft.Page):
    
    #COLORS
    bgcolor = "#100017"
    primary = "#41005E"
    secondary = "#F1DEFA"
    tertiary = "#B19FF9"
    
    #PAGE SETUP
    page.title = "Geet"
    page.horizontal_alignment = "center"
    page.bgcolor = bgcolor
    page.theme_mode = "dark"

    #ACTIONS
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
        current_song.title = ft.Text(e.control.data[0], max_lines=2, overflow="ellipsis", color=ft.colors.WHITE)
        current_song.subtitle = ft.Text(e.control.data[1], max_lines=1, overflow="ellipsis", color=ft.colors.WHITE70)
        
        #Auto-Play the song
        if page.platform != "ios" and page.platform != "macos":
            song.play()
            playpausebtn.icon = ft.icons.PAUSE_CIRCLE_ROUNDED

        #Update music player
        music_player.disabled = False

        loadbar.width = 0

        page.update()


    def listsongs(e):

        if search_box.value != "":
            loadbar.width = 450
            page.update()
            
            songdict = music.searchsong(search_box.value)

            song_list.controls.clear()

            for song in songdict['songs']:
                
                song_item = ft.ListTile(width=450)
                song_item.title = ft.Text(song['name'], color=secondary)
                song_item.subtitle = ft.Text(song['artists'], color=tertiary)
                song_item.data = [song['name'], song['artists'], song['videoId']]
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
    

    #App Bar
    app_bar = ft.AppBar(center_title=True, bgcolor=bgcolor)

    app_bar.title = ft.Text("geet", style=ft.TextThemeStyle.HEADLINE_LARGE, color=ft.colors.WHITE,
    weight="bold", italic=True, size=40)

    app_bar.actions= [ft.TextButton(icon=ft.icons.CODE, icon_color=secondary ,on_click=lambda e: page.launch_url("https://github.com/redromnon/Geet"))]


    #Loading bar
    loadbar = ft.ProgressBar(width=0, color=secondary)
    

    #Song List
    song_list = ft.Column([], spacing=10, scroll="always", expand=True, horizontal_alignment="stretch")


    #Search Box
    search_box = ft.TextField(filled=True, border_width=2, border_radius=20, 
    hint_text="Enter a song name", width=400, prefix_icon=ft.icons.SEARCH_ROUNDED,
    on_submit=listsongs, focused_border_color=secondary, focused_color=secondary,
    bgcolor=bgcolor, cursor_color=secondary, selection_color=secondary)


    #Music Player
    current_song = ft.ListTile(leading=ft.Icon(ft.icons.MUSIC_NOTE, size=40, color=secondary), title=ft.Text("...", color=ft.colors.WHITE),
    subtitle=ft.Text("...", color=tertiary), expand=True)

    playpausebtn = ft.IconButton(icon=ft.icons.PLAY_CIRCLE_ROUNDED, icon_size=30, on_click=play_pause_song, icon_color=secondary)
    
    repeatbtn = ft.IconButton(icon=ft.icons.REPEAT_ROUNDED, icon_size=30, on_click=repeat_song, icon_color=secondary)

    player_button = ft.Row(
        [
            playpausebtn, repeatbtn
        ],
        alignment="end", spacing=5
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
        app_bar,
        ft.Column(
            [
                search_box, loadbar, song_list,
            ],
            horizontal_alignment="center",
            spacing=20, expand=True
        ),
        music_player
    )


    
if __name__ == "__main__":

    #Create temp directory
    with tempfile.TemporaryDirectory() as music.tmpdir:
        print(f"Temporary directory created at {music.tmpdir}")

        #Run app
        ft.app(target=main, assets_dir=music.tmpdir, view=ft.WEB_BROWSER)

        #Cleanup
        print(f"Deleting {music.tmpdir}")