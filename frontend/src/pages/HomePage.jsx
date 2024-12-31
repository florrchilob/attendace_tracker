import React, { useState } from 'react'
import InputPage from './InputPage';
import NamePage from './NamePage';

function HomePage() {

    const [currentCard, setCurrentCard] = useState("inputCard");
    const [selectedOption, setSelectedOption] = useState("misparIshi");
    const [inputID, setInputID] = useState("");


    return (
        <>
            {currentCard == "inputCard" ?  
                <InputPage inputID={inputID} selectedOption={selectedOption} setInputID={setInputID} 
                setSelectedOption={setSelectedOption} setCurrentCard={setCurrentCard}/> 
                : 
                <NamePage inputID={inputID} selectedOption={selectedOption} setInputID={setInputID} 
                setSelectedOption={setSelectedOption} setCurrentCard={setCurrentCard}/>}
        </>
    )
}

export default HomePage