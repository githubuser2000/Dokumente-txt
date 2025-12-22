import Data.Ratio
import System.IO.Unsafe (unsafePerformIO)
import System.Random (randomR, newStdGen)

-- Minimale, kompatible Random-Funktion
randInt :: Int -> Int -> Int
randInt lo hi = unsafePerformIO $ do
    gen <- newStdGen
    let (x,_) = randomR (lo,hi) gen
    return x

-- zufällige Länge 3–20
randomLength :: IO Int
randomLength = do
    gen <- newStdGen
    let (n,_) = randomR (3,20) gen
    return n

-- zufälliges Fraction oder Int
randomRationalOrInt :: IO (Ratio Int)
randomRationalOrInt = do
    gen <- newStdGen
    let (bit,gen2) = randomR (0,1 :: Int) gen

    if bit == 0
        then do
            let (n,gen3) = randomR (1,9) gen2
                (d,_)    = randomR (1,9) gen3
            return (n % d)
        else do
            let (x,_) = randomR (1,20) gen2
            return (x % 1)

-- zufällige Liste
randomFractionList :: IO [Ratio Int]
randomFractionList = do
    len <- randomLength
    sequence (replicate len randomRationalOrInt)

------------------------------------------------------------
-- 3 Werte → 6 ints
------------------------------------------------------------

toInt :: Ratio Int -> Int
toInt r = floor (fromIntegral (numerator r)
               / fromIntegral (denominator r) * 10)

fractionTripletToSpace :: (Ratio Int,Ratio Int,Ratio Int)
                       -> (Int,Int,Int,Int,Int,Int)
fractionTripletToSpace (a,b,c) =
    let f x =
            let val  = toInt x
                minv = val
                maxv = max (val*2) val
            in (minv, maxv)
        (a1,a2) = f a
        (b1,b2) = f b
        (c1,c2) = f c
    in (a1,a2,b1,b2,c1,c2)

triplets :: [a] -> [(a,a,a)]
triplets (x:y:z:rest) = (x,y,z) : triplets rest
triplets _            = []

fractionsToSpaces :: [Ratio Int] -> [(Int,Int,Int,Int,Int,Int)]
fractionsToSpaces xs = map fractionTripletToSpace (triplets xs)

------------------------------------------------------------
-- MAIN
------------------------------------------------------------

main :: IO ()
main = do
    xs <- randomFractionList
    putStrLn "Liste:"
    print xs

    putStrLn "\nSpaces:"
    mapM_ print (fractionsToSpaces xs)

