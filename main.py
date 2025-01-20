import flet as ft

def main(pagina):
    titulo = ft.Text("Chat dos Crias")
    pagina.add(titulo)

    chat = ft.Column()

    nome_usuario = ft.TextField(label="Escreva seu nome")

    def tunel_mensagens(mensagem):
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{usuario_mensagem}: {texto_mensagem}")) # adicionar a mensagem no chat
        else:
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{usuario_mensagem} entrou no chat", size=12, italic=True, color=ft.colors.ORANGE_500))
        pagina.update()

    pagina.pubsub.subscribe(tunel_mensagens)


    def enviar_mensagem(evento):
        pagina.pubsub.send_all({"texto": campo_mensagem.value, "usuario": nome_usuario.value, "tipo": "mensagem"})
        campo_mensagem.value = "" #limpar o campo de mensagem
        pagina.update()

    campo_mensagem = ft.TextField(label="Digite uma mensagem", on_submit=enviar_mensagem)
    botao_enviar_mensagem = ft.ElevatedButton("Enviar", on_click=enviar_mensagem)


    def entrar_chat(evento):
        pagina.pubsub.send_all({"usuario": nome_usuario.value, "tipo": "entrada"})
        pagina.add(chat) #adicionar o chat
        popup.open = False #fechar o alerta
        pagina.remove(titulo)
        pagina.remove(botao_iniciar)
        pagina.add(ft.Row([campo_mensagem, botao_enviar_mensagem])) #adicionar o campo de mensagem e o botão de enviar a mensagem
        pagina.update()


    def entrar_popup(evento):
        pagina.dialog = popup
        popup.open = True
        pagina.update()

    popup = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text("Aqui a PF não nos encontra"),
        content=nome_usuario,
        actions=[ft.ElevatedButton("Entrar", on_click=entrar_chat)],
    )

    botao_iniciar = ft.ElevatedButton("Iniciar chat", on_click=entrar_popup)
    pagina.add(botao_iniciar)
    
    
ft.app(target=main, view=ft.WEB_BROWSER, port=8000)
