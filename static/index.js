import { clearContentContainer, fetchAndDisplayDailyGames, resetButtonStyles, fetchAndDisplayTopPerformers,
        fetchAndDisplayInjuryReport, showLoadingScreen, hideLoadingScreen } from './functions.js';

const dailyGamesBtn = document.getElementById("daily-games-btn")
const topPerformersBtn = document.getElementById("top-performers-btn")
const injuryReportBtn = document.getElementById("injury-report-btn")
const contentContainer = document.getElementById("contentContainer")
const contentPlaceholderDiv = document.getElementById("content-container-placeholder-div")
const loadingScreen = document.getElementById("loadingScreen");
const placeholderContent = document.getElementById('placeholder-content');



document.addEventListener("DOMContentLoaded", function() {

    function handleButtonClick(buttonElement, contentDisplayFunction) {
        
        
        
    

        resetButtonStyles();
        clearContentContainer();
        contentDisplayFunction();
        buttonElement.style.backgroundColor = 'lightblue';
       
    
    }
    dailyGamesBtn.addEventListener("click", function() {
        
        handleButtonClick(dailyGamesBtn, fetchAndDisplayDailyGames);
    });

    topPerformersBtn.addEventListener("click", function() {
        handleButtonClick(topPerformersBtn, fetchAndDisplayTopPerformers);
    });

    injuryReportBtn.addEventListener("click", function() {
        handleButtonClick(injuryReportBtn, fetchAndDisplayInjuryReport)
    });

});





