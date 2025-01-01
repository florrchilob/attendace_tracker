import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import InputPage from './InputPage';
import NamePage from './NamePage';

function HomePage() {
  const [currentCard, setCurrentCard] = useState("inputCard");
  const [selectedOption, setSelectedOption] = useState("misparIshi");
  const [inputID, setInputID] = useState("");

  const pageVariants = {
    initial: (direction) => ({
      x: direction > 0 ? "100%" : "-100%",
      opacity: 0,
    }),
    animate: {
      x: 0,
      opacity: 1,
      transition: {
        type: "tween", 
        duration: 0.3,
      },
    },
    exit: (direction) => ({
      x: direction > 0 ? "-100%" : "100%",
      opacity: 0,
      transition: {
        type: "tween",
        duration: 0.3,
      },
    }),
  };

  const [direction, setDirection] = useState(1);

  const switchToInputCard = () => {
    setDirection(-1);
    setCurrentCard("inputCard");
  };

  const switchToNameCard = () => {
    setDirection(1);
    setCurrentCard("nameCard");
  };

  return (
    <div dir="rtl" className="relative bg-bg-desktop bg-cover bg-center h-screen w-screen flex justify-center items-center overflow-hidden">
      <AnimatePresence custom={direction} mode="wait">
        {currentCard === "inputCard" ? (
          <motion.div
            key="inputCard"
            custom={direction}
            initial="initial"
            animate="animate"
            exit="exit"
            variants={pageVariants}
            className="w-full px-36 py-auto my-auto items-center h-full py-auto flex flex-col"
          >
            <InputPage
              inputID={inputID}
              selectedOption={selectedOption}
              setInputID={setInputID}
              setSelectedOption={setSelectedOption}
              setCurrentCard={switchToNameCard}
            />
          </motion.div>
        ) : (
          <motion.div
            key="nameCard"
            custom={direction}
            initial="initial"
            animate="animate"
            exit="exit"
            variants={pageVariants}
            className="w-full px-36 py-auto my-auto items-center h-full py-auto flex flex-col"
          >
            <NamePage
              inputID={inputID}
              selectedOption={selectedOption}
              setInputID={setInputID}
              setSelectedOption={setSelectedOption}
              setCurrentCard={switchToInputCard}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default HomePage;
