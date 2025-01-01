import {React, useEffect, useState} from 'react'
import errorGif from '../assets/gifs/error-page.gif'

const ErrorPage = () => {


  return (
    <>
      <div className='flex flex-col transition-all duration-700 h-full mt-4 sm:inline smoverflow-hidden my-auto'>
        <div className='transition-all duration-700 px-5 py-3 flex flex-col h-full bg-backgroundColor shadow-shadowColor 
        shadow-customShadow bg-opacity-backgroundOpacity rounded-customRounded overflow-hidden'>
          <img 
            src={errorGif} 
            id="animation-gif" 
            className={`flex justify-center mt-[-400px] mb-[-390px] w-[900px] `} 
            style={{ height: 'auto' }}
          />

          <p className={`font-threeThinner sm:h-14 sm:mb-0 px-2 text-redConvinedStronger text-center rounded-customRounded sm:text-desktopGeneral2
          w-full mx-auto text-2xl outline-none grow border-none text-customText mt-11 sm:mt-0`}> יש לנו תקלה טכנית כעת, נסו שוב מאוחר יותר.</p>
        </div>
      </div>
    </>
  )
}

export default ErrorPage