if __name__ == '__main__':
    from app import create_app

    app = create_app()

    # secret key for session
    app.secret_key = 'super secret key'

    app.run(host='0.0.0.0', port=3000)
