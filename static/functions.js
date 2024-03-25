const dailyGamesBtn = document.getElementById("daily-games-btn")
const topPerformersBtn = document.getElementById("top-performers-btn")
const injuryReportBtn = document.getElementById("injury-report-btn")
const contentContainer = document.getElementById("contentContainer")


export function clearContentContainer() {

    while (contentContainer.firstChild) {
        contentContainer.removeChild(contentContainer.firstChild);
    }
}



export function resetButtonStyles() {

    dailyGamesBtn.style.backgroundColor = '';
    topPerformersBtn.style.backgroundColor = '';
    injuryReportBtn.style.backgroundColor = '';

}


export function showLoadingAnimation() {
    document.getElementById('loadingAnimation').style.display = 'block';
}

// Function to hide loading animation
export function hideLoadingAnimation() {
    document.getElementById('loadingAnimation').style.display = 'none';
}

export function showLoadingScreen() {
    loadingScreen.style.display = "block";
    setTimeout(function() {
        hideLoadingScreen();
    }, 1000); 
}

export function hideLoadingScreen() {
    loadingScreen.style.display = "none";
}





export function fetchAndDisplayDailyGames() {
    fetch('http://127.0.0.1:5000/api/daily-games')
    .then(response => {
        if (!response.ok) {
        throw new Error('Network response was not ok');
        }
        return response.json();
        })
    .then(data => {
        
        const contentContainer = document.getElementById('contentContainer');

        data.forEach(game => {
            const gameDiv = document.createElement('div');
            gameDiv.classList.add('game'); 
    
            const gameDetailsList = document.createElement('ul');
            gameDetailsList.classList.add('game-details', 'squada-one', 'content-list-fs'); 
    
            let homeVsAway = document.createElement('li');
    
            if (game.gameStatus === 'Live - In Progress') {
                const gameStatus = document.createElement('li');
                const gameClock = document.createElement('li');
                homeVsAway.textContent = `${game.home}: ${game.homePts} vs ${game.away}: ${game.awayPts}`;
                gameStatus.textContent = `${game.gameStatus}`;
                gameClock.textContent = `${game.gameClock}`;
    
                // Append list items to the list
                gameDetailsList.appendChild(homeVsAway);
                gameDetailsList.appendChild(gameStatus);
                gameDetailsList.appendChild(gameClock);
            } else {
                homeVsAway.textContent = `${game.home} vs ${game.away}`;
                const gameTime = document.createElement('li');
                gameTime.textContent = `Start: ${game.gameTime}m`;
    
                // Append list items to the list
                gameDetailsList.appendChild(homeVsAway);
                gameDetailsList.appendChild(gameTime);
            }
    
            // Append the list to the game div
            gameDiv.appendChild(gameDetailsList);
    
            // Append the game div to the content container
            contentContainer.appendChild(gameDiv);
        });
        
    })
    .catch(error => {
    
        console.error('There was a problem with the fetch operation:', error);
    });

    
}


export function fetchAndDisplayTopPerformers() {
    fetch('http://127.0.0.1:5000/api/top-performers')
    .then(response => {
        if (!response.ok) {
        throw new Error('Network response was not ok');
        }
        return response.json();
        })
    .then(data => {
        
        const contentContainer = document.getElementById('contentContainer');

        data.forEach((player, index) => {
            const playerContainer = document.createElement('div');
            playerContainer.classList.add('player-container');
            const playerNameAndImage = document.createElement('div');
            playerNameAndImage.classList.add("top-performer-name-img-container");

            const nameAndList = document.createElement('div');
            playerNameAndImage.appendChild(nameAndList);

            // Create player name element
            const playerName = document.createElement('h2');
            playerName.classList.add("top-performer-name");
            playerName.textContent = `${index + 1} | ${player.player_name}`;
            nameAndList.appendChild(playerName);

            // Create player image element
            const playerImage = document.createElement('img');
            playerImage.classList.add("top-performer-img")
            playerImage.src = player.nbaComHeadshot;
            playerImage.alt = player.longName + ' Image';
            playerNameAndImage.appendChild(playerImage);

            playerContainer.appendChild(playerNameAndImage)


            

            // Create player stats list
            const statsList = document.createElement('ul');
            statsList.classList.add("statsList")
            nameAndList.classList.add('player-stats');

            // Add relevant player stats to the list
            const relevantStats = ['pts', 'reb', 'ast', 'stl', 'blk'];
            relevantStats.forEach(stat => {
                const statItem = document.createElement('li');
                statItem.textContent = `${stat.toUpperCase()}: ${player.stats[stat]}`;
                statsList.appendChild(statItem);
            
            });

            // Append stats list to the player container
            nameAndList.appendChild(statsList);

            const hr = document.createElement('hr')
            hr.classList.add("hr-top-performers")

            if (index == 4) {
                contentContainer.appendChild(playerContainer);
            } else {
                playerContainer.appendChild(hr)
                contentContainer.appendChild(playerContainer);
            }

            // Append player container to the content container
            
        });
        

    })
    .catch(error => {
    
        console.error('There was a problem with the fetch operation:', error);
    });
}




export function fetchAndDisplayInjuryReport() {
    fetch('http://127.0.0.1:5000/api/injury-report')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const contentContainer = document.getElementById('contentContainer');

        data.forEach(player => {
            
            const injuredPlayerContainer = document.createElement('div');
            injuredPlayerContainer.classList.add('injured-player-container');

            const playerImage = document.createElement('img');
            playerImage.classList.add("injured-player-img")
            playerImage.src = player.nbaComHeadshot;
            playerImage.alt = player.player_name + ' Image';
            injuredPlayerContainer.appendChild(playerImage);
            
            const injuryDetailsList = document.createElement('ul');
            injuryDetailsList.classList.add('injury-details-list');

            const playerNameItem = document.createElement('li');
            playerNameItem.textContent = `Player Name: ${player.player_name}`;

            const teamCodeItem = document.createElement('li');
            teamCodeItem.textContent = `Team Code: ${player.team_code}`;

            const injDate = player.injDate;
            const formattedInjDate = `${injDate.substr(6, 2)}/${injDate.substr(4, 2)}/${injDate.substr(0, 4)}`;

            const injDateItem = document.createElement('li');
            injDateItem.textContent = `Injury Date: ${formattedInjDate}`;

            const designationItem = document.createElement('li');
            designationItem.textContent = `Designation: ${player.designation}`;

            const descriptionItem = document.createElement('li');
            descriptionItem.textContent = `${player.description}`;



            injuryDetailsList.appendChild(playerNameItem);
            injuryDetailsList.appendChild(teamCodeItem);
            injuryDetailsList.appendChild(injDateItem);
            injuryDetailsList.appendChild(designationItem);
            injuryDetailsList.appendChild(descriptionItem);
            
            injuredPlayerContainer.appendChild(injuryDetailsList);

            
            contentContainer.appendChild(injuredPlayerContainer);
        });
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}