import os

answer = (
    str(input("Would you like to turn on debug mode?\ntype yes or no ")).lower().strip()
)

if answer == "yes" or answer == "y":
    os. = "development"
else:
    del os.environ["CDAPYTHON_ENV"]



unset CDAPYTHON_ENV 