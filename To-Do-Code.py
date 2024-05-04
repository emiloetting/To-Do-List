#importe
import sys
import pickle
import os
import msvcrt
from prompt_toolkit import prompt
#   ignore
'''-----------------------------------------------------------------------------------------------------'''
list_of_all_todos = []
path =os.getcwd() #<= hier pfad
try:
    with open(os.path.join(path, "todolists.pkl"), "rb") as f:
            list_of_all_todos=pickle.load(f)
except FileNotFoundError:
        print("File Not found - Keine Listen gefunden")
'''-----------------------------------------------------------------------------------------------------'''
#sidequests
def back_to_main_menu():
    print("Drücken Sie eine beliebige Taste, um zum Hauptmenü zurückzukehren.")
    msvcrt.getch()  
    print() 

def safe_changes():
    try: 
        pickle.dump(list_of_all_todos, open(os.path.join(path, "todolists.pkl"), "wb"))
        print('\nÄnderungen erfolgreich gespeichert!')
        back_to_main_menu()
    except Exception:
        print("\nÄnderungen konnten nicht gespeichert werden!")
        back_to_main_menu()
 
#main menu stuff
def create_new_todo():
    print(80*'-','\n')
    choice_name=input('Gib deiner Liste einen Namen\n>>>')
    choice_name.strip()
    if choice_name=='':
        name_new_list='Neue Liste'
    else:
        name_new_list=choice_name
    for list in list_of_all_todos:
        while name_new_list==list[0]:
            name_new_list=input('Name bereits vergeben, wähle einen anderen\n>>>')
    input_for_list=input('Starte deine neue Liste! Trenne deine Unterpunkte durch Kommata!\n>>>')
    list_new_list = [x.strip() for x in input_for_list.split(',')]
    tupel_new_list=(name_new_list, list_new_list)
    list_of_all_todos.append(tupel_new_list)
    show_all_todos()
    while True:
            print('Möchtest du eine weitere Liste erstellen?\n\t[0] Ja\n\t[1] Nein, zurück zum Hauptmenu\n')
            match msvcrt.getch():
                case b'0':  
                    return create_new_todo()
                case b'1':
                    break
                case _:
                    print("Ungültige Eingabe")

def show_all_todos():
    print(80*'-','\n')
    print('Eine Übersicht deiner Listen:\n')
    if list_of_all_todos!=[]:
        for index, todo in enumerate(list_of_all_todos, start=1):
            list_name, actual_list = todo
            try:
                print(f'[{index}] {list_name}:\n\t{", ".join(map(str, actual_list))}\n')
            except Exception:
                print(f'Die Liste "{list_name}" ist noch leer!\n')
                back_to_main_menu()
    else:
        print('Keine Liste gefunden!')
        while True:
            print('Möchtest du eine Liste erstellen?\n\t[0] Ja\n\t[1] Nein, zurück zum Hauptmenu\n>>>')
            match msvcrt.getch():
                case b'0':  
                    return create_new_todo()
                case b'1':
                    break
                case _:
                    print("Ungültige Eingabe")
    
def edit_todo():
    while True:
        show_all_todos()
        print('Welche Liste möchtest du bearbeiten? (Drücke 0, um zurück zum Hauptmenu gelangen)')
        while msvcrt.kbhit():   #damit der Puffer geleert wird und bei falscher Eingabe eine erneute Eingbe mögl. ist
            msvcrt.getch()
        choice_to_edit=msvcrt.getch()
        if choice_to_edit==b'0':
            break
        try:
            choice_to_edit=int(choice_to_edit)-1
            if choice_to_edit in range(len(list_of_all_todos)):
                chosen_list_name=list_of_all_todos[choice_to_edit][0]
                chosen_list_list=list_of_all_todos[choice_to_edit][1]
                print(chosen_list_name,'\n')
                while True:
                    print(chosen_list_name)
                    for index, unterpunkt in enumerate(chosen_list_list, start=1):
                        print(f'[{index}]: {unterpunkt}')
                    print('\nMöchtest du:\n\t[1] Unterpunkt(e) löschen\n\t[2] Unterpunkt(e) hinzufügen\n\t[3] Unterpunkt bearbeiten\n')
                    match msvcrt.getch():
                        case b'1':
                            aspects_to_delete=[value.strip() for value in input('Welche Unterpunkte möchtest du löschen? Gib die Indizes an und trenne sie durch Kommata\n').split(',')]
                            while '0' in aspects_to_delete:
                                print('\nUngültige Eingabe!\nStelle sicher, dass du die ensprechenden Indizes verwendest\n')
                                aspects_to_delete=[value.strip() for value in input('Welchen Unterpunkte möchtest du löschen? Gib die Indizes an und trenne sie durch Kommata\n').split(',')]
                            print('\nFolgende Unterpunkte hast du ausgewählt:')
                            try:
                                print('\n'.join(f'\t[x] {chosen_list_list[int(aspect)-1]}' for i, aspect in enumerate(aspects_to_delete)))
                                print('\nMöchtest du diese Unterpunkte löschen?\n\t[0] Ja\n\t[1] Nein\n')
                                while True:
                                    match msvcrt.getch():
                                        case b'0':
                                            for aspect in reversed(aspects_to_delete):
                                                value_to_remove = chosen_list_list[int(aspect)-1]
                                                if value_to_remove in list_of_all_todos[choice_to_edit][1]:
                                                    list_of_all_todos[choice_to_edit][1].remove(value_to_remove)
                                                else:
                                                    print(f'"{value_to_remove}" wurde nicht gefunden')
                                            if list_of_all_todos[choice_to_edit][1]==[]:
                                                print('Herzlichen Glückwunsch!')
                                                while True:
                                                    print('Die Liste wurde abgearbeitet.\nMöchtest du sie jetzt löschen?\n\t[0] Ja\n\t[1] Nein')
                                                    match msvcrt.getch():
                                                        case b'0':
                                                            del list_of_all_todos[choice_to_edit]
                                                            print('\nDie Liste wurde gelöscht!')
                                                            break
                                                        case b'1':
                                                            print('\nAlles klar, die Liste bleibt erhalten!')
                                                            break
                                                        case _:
                                                            print('Ungültige Eingabe')
                                            break           
                                        case b'1':
                                            back_to_main_menu()
                                            return main_menu()
                                        case _:
                                            print('Ungültige Eingabe') 
                                break
                            except Exception:
                                print('Ungültige Eingabe!\nStelle sicher, dass du gültige Indizes angibst')
                        case b'2':
                            aspects_to_add=[aspect.strip() for aspect in input('\nWelche Punkte möchtest du zur Liste hinzufügen?\nTrenne deine Eingaben durch Kommata!\n\t>>>').split(',')]
                            chosen_list_list.extend(aspects_to_add)
                            print(f'\nListe {chosen_list_name} wurde geupdated!\n')
                            for index, unterpunkt in enumerate(chosen_list_list, start=1):
                                print(f'\t[{index}]: {unterpunkt}')
                            break
                        case b'3':
                            while True:
                                try:
                                    aspect_to_edit = (int(input('Welchen Unterpunkt möchtest du bearbeiten? Gib einen Index an!\n>>>'))-1)
                                    if aspect_to_edit > 0 and aspect_to_edit <= len(chosen_list_list):
                                        break
                                    else:
                                        print("Ungültiger Eingabe. Wähle einen gültigen Index")
                                except ValueError:
                                    print("Ungültige Eingabe. Achte auf korrekte Indexierung.")
                            aspect_edited=prompt("Bearbeite deinen Unterpunkt: ", default=chosen_list_list[aspect_to_edit])
                            chosen_list_list[aspect_to_edit]=aspect_edited
                            print('Die Änderung wurde übernommen!\nHier deine aktualisierte Liste\n')
                            print(chosen_list_name)
                            for index, unterpunkt in enumerate(chosen_list_list, start=1):
                                print(f'\t[{index}]: {unterpunkt}')
                            back_to_main_menu()
                            break
                        case _:
                            print('Ungültige Eingabe!\n')
                break
            else:
                print('Ungültige Eingabe!\nVerwende die entsprechenden Indizes')
        except Exception:
            print('Ungültige Eingabe!\nStelle sicher, dass du die entsprechenden Indizes verwendest')

def delete_todo():
    show_all_todos()
    print('Welche Liste möchtest du entfernen? Drücke (0), um zurück zum Hauptmenu zu gelangen')
    to_delete=int(msvcrt.getch())
    if to_delete != 0:
        while True:
            while True:
                print(f'Möchtest du Liste Nr. {to_delete} wirklich entfernen?\n    [0] Ja\n    [1] Nein\n>>>')
                try:
                    check_before_delete=int(msvcrt.getch())
                    break
                except Exception:
                    print('Ungültiger Input!')
            match check_before_delete:
                case 0:
                    try:
                        del list_of_all_todos[to_delete-1]
                        while True and list_of_all_todos!=[]:
                            print('Möchtest du eine weitere Liste löschen?\n\t[0] Ja\n\t[1] Nein')
                            match msvcrt.getch():
                                case b'0':
                                    return delete_todo()
                                case b'1':
                                    return show_all_todos()
                                case _:
                                    print('Ungültige Eingabe')
                    except IndexError:
                        print('Ungültige Eingabe')
                        return delete_todo()
                case 1:
                    while True:
                        print('Möchtest du\n\t[0] eine andere Liste löschen\n\t[1] zurück zum Hauptmenü\n')
                        match msvcrt.getch():
                            case b'0':
                                return delete_todo()
                            case b'1':
                                break
                            case _:
                                print('Ungültige Eingabe')       
                    break  
                case _:
                    print('Ungültige Eingabe')            

def main_menu():
    while True:
        show_main_menu()
        print('Wähle eine Nummer (1-5) aus')
        match msvcrt.getch():
            case b'1':
                create_new_todo()
                safe_changes()
            case b'2':
                show_all_todos()
                back_to_main_menu()
            case b'3':
                edit_todo()
                safe_changes()
            case b'4':
                delete_todo()
                safe_changes()
            case b'5':
                pickle.dump(list_of_all_todos, open(os.path.join(path, "todolists.pkl"), "wb"))
                break
            case _:
                print('Ungültige Eingabe')
            
def show_main_menu():
    print(80*'-','\n')
    print('Willkommen zur HSD DAISY TO-DO Listen Applikation: Was möchten Sie tun?\n \n')
    print('    (1) Eine neue TO-DO Liste anlegen')
    print('    (2) Alle TO-DO Listen anzeigen')
    print('    (3) Eine TO-DO Liste zum Bearbeiten auswählen')
    print('    (4) Eine TO-DO Liste löschen')
    print('    (5) Die Applikation beenden\n')

'''-----------------------------------------------------------------------------------------------------'''
if __name__ == '__main__':
    main_menu()
    print('Sie haben die App verlassen.\nAuf Wiedersehen')
    sys.exit()
