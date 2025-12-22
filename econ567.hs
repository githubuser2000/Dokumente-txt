{-# LANGUAGE ScopedTypeVariables #-}
module Main where
import Data.Ratio
import Data.List
import Text.Printf

-- ***************************************************************
-- Basisfunktionen
-- ***************************************************************

-- Primfaktorzerlegung: n → [(p,e)]
primeFactors :: Integer -> [(Integer, Int)]
primeFactors n = factor n 2
  where
    factor 1 _ = []
    factor m p
      | p * p > m = [(m,1)]
      | m `mod` p == 0 =
          let (count, rest) = countPowers m p 0
          in (p, count) : factor rest (p+1)
      | otherwise = factor m (p+1)

    countPowers m p c
      | m `mod` p /= 0 = (c, m)
      | otherwise = countPowers (m `div` p) p (c+1)

-- Rekonstruktion aus Primfaktoren
fromPrimeFactors :: [(Integer, Int)] -> Integer
fromPrimeFactors = foldr (\(p,e) acc -> acc * p^e) 1

-- Operation P: Exponenten +1
pOp :: Integer -> Integer
pOp n = fromPrimeFactors [(p, e+1) | (p,e) <- primeFactors n]

-- Operation Q: Quotientbildung
qOp :: Integer -> Integer -> Rational
qOp a b = a % b

-- Operation P auf rationalem Bruch
pFrac :: Rational -> Rational
pFrac r =
    let num = numerator r
        den = denominator r
    in (pOp num) % (pOp den)

-- Erzeugt die sechs Kernzahlen
zahlensystem :: Integer -> (Integer, Integer, Rational, Rational, Rational, Rational)
zahlensystem n1 =
    let n2 = pOp n1
        q1 = qOp n1 n2
        q2 = qOp n1 n2
        q3 = pFrac q1
        q4 = pFrac q2
    in (n1, n2, q1, q2, q3, q4)

-----------------------------------------------------------------------
-- Hilfsfunktionen für Skalierung und Winkel
-----------------------------------------------------------------------

-- Rational → Double
ratToDouble :: Rational -> Double
ratToDouble r = fromIntegral (numerator r) / fromIntegral (denominator r)

-- Rational → String im Format "Zähler / Nenner" (ersetzt %)
formatRational :: Rational -> String
formatRational r = show (numerator r) ++ " / " ++ show (denominator r)

-- 1. Hauptwinkel in Grad
baseAngleDeg :: Rational -> Double
baseAngleDeg r = atan (ratToDouble r) * (180 / pi)

-- 2. Orthogonaler Winkel
orthogonalAngleDeg :: Rational -> Double
orthogonalAngleDeg r =
    let recipR = denominator r % numerator r
    in baseAngleDeg recipR - 180

-- 3. Komplementärwinkel
complementaryAngleDeg :: Rational -> Double
complementaryAngleDeg r = 90 - baseAngleDeg r

-- GENERIERT DIE 48 SKALIERUNGSERGEBNISSE
generate48Scales :: [Integer] -> [Integer] -> [Double]
generate48Scales nList qPartsList =
    let
        nDoubles = map fromIntegral nList
        qDoubles = map fromIntegral qPartsList

        -- Produkte (3 * 8 = 24 Ergebnisse)
        products = [n * q | n <- nDoubles, q <- qDoubles]

        -- Divisionen (3 * 8 = 24 Ergebnisse)
        -- ACHTUNG: Division durch 0 (falls ein Nenner 0 wäre) wird hier nicht abgefangen.
        divisions = [n / q | n <- nDoubles, q <- qDoubles]

    in products ++ divisions

-----------------------------------------------------------------------
-- Endausgabe
-----------------------------------------------------------------------

main :: IO ()
main = do
    let (n1, n2, q1, q2, q3, q4) = zahlensystem 12
        
        -- Platzhalter für n3 (wie in der Anforderung $n_1, n_2, n_3$)
        n3 = n1 
        common = n1
        
        -- Liste der 3 Zahlen
        nList = [n1, n2, n3]
        
        -- Liste der 8 Bruchteile
        qParts = [numerator q1, denominator q1, numerator q2, denominator q2,
                  numerator q3, denominator q3, numerator q4, denominator q4]

        -- Berechne alle 48 Skalierungsergebnisse
        scales48 = generate48Scales nList qParts
        
        qs = [q1, q2, q3, q4]
        
        -- Die 8 Werte als Strings für die Beschriftung (mit /)
        values = [
            (show n1), (show n2), (show n3), (show common), 
            (formatRational q1), (formatRational q2), (formatRational q3), (formatRational q4)
            ]

        labels = [
            "Wert Geld Währung Nummer Zahlen Wert Währung (folgende sind Währungen von nicht Nummern Zahlen Werten)",
            "Gutartigkeit Selbstlosigkeit Führungsschicht Regierung Herrschaft",
            "Ganzheit Kaputtheit Nicht-Armut Zentralität Unterschicht",
            "Primfaktor-Zerlegungs-Verwandschafts-Gemeinsamkeit dreier positiver zufälliger ganzer Natürlicher Zahlen Zahl",
            "Verhältnis Wert zu Führungsschicht, Gutartigkeit Produkt, Firma, Leistung als Winkel-Richtung",
            "Wert Verhältnis zu Unterschicht, Kaputtheit Armut Ganzheit Gesundheit zum Wert statt ins Verhältnis eine Skalierung",
            "Führungsschicht Regierer Parteien gegenüber Unterschicht Relation Verhältnis oder als Skarierung gemeint und zu verstehen, entweder oder",
            "Unterschicht Verhältnis zu Führungsschicht Regierung Herrscher Relation Verhältnis, oder als Skarierung gemeint und zu verstehen, entweder oder"
            ]

    putStrLn "--- ABSCHNITT 1: Beschriftete Werte (8 Ausgaben) ---"
    mapM_ (\(l, v) -> putStrLn $ l ++ ": " ++ v) (zip labels values)
    putStrLn ""
    putStrLn "----------------------------------------------------"
    putStrLn ""

    -- ABSCHNITT 2: Winkelberechnungen (12 Ausgaben, beibehalten auf Wunsch)
    let angleBase  = map baseAngleDeg qs
        angleOrtho = map orthogonalAngleDeg qs
        angleComp  = map complementaryAngleDeg qs

    putStrLn "--- ABSCHNITT 2: Winkelberechnungen (Alle 2 Nachkommastellen) ---"

    putStrLn "\n1. Basiswinkel (Arcustangens des Quotienten):"
    mapM_ (\(i,a) -> printf "q%d = %.2f°\n" (i :: Int) a)
          (zip [1..4] angleBase)

    putStrLn "\n2. Orthogonalwinkel (−180°, Reziprok):"
    mapM_ (\(i,a) -> printf "q%d = %.2f°\n" (i :: Int) a)
          (zip [1..4] angleOrtho)

    putStrLn "\n3. Komplementärwinkel (90° - Basiswinkel):"
    mapM_ (\(i,a) -> printf "q%d = %.2f°\n" (i :: Int) a)
          (zip [1..4] angleComp)
    
    putStrLn ""
    putStrLn "----------------------------------------------------"
    putStrLn ""

    -- ABSCHNITT 3: Skalierungsberechnungen (48 Ausgaben)
    let nNames = ["n1", "n2", "n3"]
        qPartNames = ["Zähler q1", "Nenner q1", "Zähler q2", "Nenner q2",
                      "Zähler q3", "Nenner q3", "Zähler q4", "Nenner q4"]

    putStrLn "--- ABSCHNITT 3: 48 Skalierungsergebnisse (3 Zahlen * 8 Bruchteile * 2 Operationen) ---"

    -- 1. Produkte (24 Ergebnisse)
    putStrLn "\n1. MULTIPLIKATION (24 Ergebnisse):"
    mapM_ (\(i, nName) -> do
        let start = i * 8
            end = start + 8
            results = take 8 (drop start scales48)
        
        putStrLn $ "  --- Ergebnisse für " ++ nName ++ " (" ++ show (nList !! i) ++ ") ---"
        mapM_ (\(qName, res) -> printf "    %s * %s = %.2f\n" nName qName res)
              (zip qPartNames results)
    ) (zip [0..2] nNames)

    -- 2. Divisionen (24 Ergebnisse)
    putStrLn "\n2. DIVISION (24 Ergebnisse):"
    mapM_ (\(i, nName) -> do
        let start = 24 + i * 8 -- Startet bei 24 (nach den Produkten)
            results = take 8 (drop start scales48)
        
        putStrLn $ "  --- Ergebnisse für " ++ nName ++ " (" ++ show (nList !! i) ++ ") ---"
        mapM_ (\(qName, res) -> printf "    %s / %s = %.2f\n" nName qName res)
              (zip qPartNames results)
    ) (zip [0..2] nNames)
    
    putStrLn "\n----------------------------------------------------"
