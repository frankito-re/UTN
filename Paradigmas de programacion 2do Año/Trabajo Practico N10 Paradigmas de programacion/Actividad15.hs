import Data.Char (isUpper)

quitarMinusculas :: String -> String
quitarMinusculas texto = [c | c <- texto, isUpper c]

main :: IO()
main = print (quitarMinusculas "Hola Mundo, no me gusta haskell")