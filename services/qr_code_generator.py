import qrcode


def generate_qr_code(data, path, filename):
    """
    This function generates a QR Code and saves it in the specified directory
    :param data:
    :param path:
    :param filename:
    :return:
    """
    print(f'Generating QR Code for {data}...')
    # Creating a QRCode object of the size specified by the user
    qr = qrcode.QRCode(version=10,
                       box_size=10,
                       border=5)
    qr.add_data(data)  # Adding the data to be encoded to the QRCode object
    qr.make(fit=True)  # Making the entire QR Code space utilized
    img = qr.make_image()  # Generating the QR Code
    filedirec = path + filename  # Getting the directory where the file has to be saved
    img.save(f'{filedirec}.png')  # Saving the QR Code
    print(f'QR Code saved at {filedirec}.png')
