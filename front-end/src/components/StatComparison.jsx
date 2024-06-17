import React, { useState } from 'react';
import { Box } from '@chakra-ui/react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);



function Stat(props) {
  const [stats, setStats] = useState([]);

  let url= 'http://127.0.0.1:8000/politician/' + props.name;
    fetch(url)
    .then(response => {
      return response.json();
    })
    .then(stats => {
      setStats(stats);
    })
    .catch(error => {
    });

  let array = new Array()
  for(let i = 30; i >= 0; i--)
    array.push(i);
  array.push('Hoy');
  let data = {
        labels: array,
        datasets: [
          {
            label: props.name,
            data: stats,
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
          },
          {
            label: 'Joe Biden',
            data: [2,2,2,2],
            borderColor: 'rgb(72, 177, 144)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
          },
        ],
      };
      
      let options = {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: false,
            text: 'Chart.js Line Chart',
          },
        },
        y: {
            min: 0,
            max: 100,
        },
      };
      
  return (
    <Box width="40vw">
      <Line data={data} options={options} />
    </Box>
  );
}

export default Stat;
