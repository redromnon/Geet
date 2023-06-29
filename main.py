import flet as ft
import music

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
    music.createcache()


    def play(e):
        
        loadbar.width = 450
        page.update()

        #Release resources and clear cache
        song.release()
        music.resetcache()

        #Download via videoId, set the new song src & display duration
        music.dmusic(e.control.data[2])
        song.src = url + music.getaudio()
        
        #Update music player
        current_song.title = ft.Text(e.control.data[0], max_lines=2, overflow="ellipsis", color=ft.colors.WHITE)
        current_song.subtitle = ft.Text(f"{e.control.data[3]} - {e.control.data[1]}", max_lines=1, overflow="ellipsis", color=ft.colors.WHITE70)
        
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
                song_item.subtitle = ft.Text(f"{song['duration']} - {song['isExplicit']}{song['artists']}", color=tertiary)
                song_item.data = [song['name'], song['artists'], song['videoId'], song['duration']]
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

    def track_progress(e):

        duration_progress.value = int(e.data)/song.get_duration()
        page.update()


    #UI COMPONENTS
    
    #Audio
    url = "../"
    song = ft.Audio(src=url+music.getaudio(), autoplay=False, on_state_changed=checkstatus, on_position_changed=track_progress)
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
    duration_progress = ft.ProgressRing(stroke_width=5, width=45, height=45, value=0, color=secondary, bgcolor=bgcolor)

    current_duration = ft.Stack(
        [
            ft.Container(content=ft.Icon(name=ft.icons.MUSIC_NOTE_ROUNDED, size=30, color=secondary), left=8, top=7),
            duration_progress,
        ]
    )

    current_song = ft.ListTile(
        leading=current_duration,
        title=ft.Text("...", color=ft.colors.WHITE),
        subtitle=ft.Text("...", color=tertiary), expand=True
    )
    
    playpausebtn = ft.IconButton(icon=ft.icons.PLAY_CIRCLE_ROUNDED, icon_size=30, on_click=play_pause_song, icon_color=secondary, tooltip="Play/Pause")
    
    repeatbtn = ft.IconButton(icon=ft.icons.REPEAT_ROUNDED, icon_size=30, on_click=repeat_song, icon_color=secondary, tooltip="Repeat")

    forwardbtn = ft.IconButton(
        icon=ft.icons.FAST_FORWARD_ROUNDED, icon_size=30, 
        on_click=lambda e: song.seek(song.get_current_position()+5000), 
        icon_color=secondary,
        tooltip="Move forward 5 sec"
    )

    rewindbtn = ft.IconButton(
        icon=ft.icons.FAST_REWIND_ROUNDED, icon_size=30, 
        on_click=lambda e: song.seek(song.get_current_position()-5000), 
        icon_color=secondary,
        tooltip="Move back 5 sec"
    )

    player_button = ft.Row(
        [
            playpausebtn, rewindbtn, forwardbtn, repeatbtn
        ],
        alignment="end", spacing=0
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


    
ft.app(target=main, assets_dir="cache", view=ft.WEB_BROWSER, port=8080)