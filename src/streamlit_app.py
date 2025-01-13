from controllers.streamlit_ctrl import StreamlitController

def main():
    controller = StreamlitController()
    controller.render_post_generator()

if __name__ == "__main__":
    main()