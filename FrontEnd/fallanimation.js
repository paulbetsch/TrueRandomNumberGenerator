function createSnowflake() {
    const snowflake = document.createElement('span');
    const randomNumber = Math.floor(Math.random() * 2); // Generate random number (0 or 1)
    snowflake.textContent = randomNumber.toString(); // Convert number to string
    snowflake.style.position = 'absolute';
    snowflake.style.top = '-50px';
    snowflake.style.left = `${Math.random() * 100}%`;
    snowflake.style.opacity = `${Math.random() * 0.5 + 0.5}`;
    snowflake.style.transition = 'all 3s linear';
    document.getElementById('snow-container').appendChild(snowflake);
    setTimeout(() => {
      snowflake.style.top = '100%';
      snowflake.style.opacity = '0';
    }, 10);
    setTimeout(() => {
      snowflake.remove();
    }, 3010);
  }
  
  setInterval(createSnowflake, 120);
  
