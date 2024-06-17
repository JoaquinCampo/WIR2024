import React from 'react';
import { Box } from '@chakra-ui/react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);



function Stat(props) {
  let array = new Array()
  for(let i = 30; i >= 0; i--)
    array.push(i);
  array.push('Hoy');
    let data = {
        labels: array,
        datasets: [
          {
            label: props.name,
            data: [65, 59, , 80, 81, 56, 55, 40],
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
          }
        ],
      };
      
      let options = {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Registro de reputaciones del último mes',
          },
        },
        y: {
            min: 0,
            max: 100,
        },
      };
      
  return (
    <Box width="600px" height="400px">
      <Line data={data} options={options} />
    </Box>
  );
}

export default Stat;
