import React from 'react';
import { Box } from '@chakra-ui/react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function Stat() {
    let data = {
        labels: ['6 days ago', '5 days ago', '4 days ago', '3 days ago', '2 days ago', '1 days ago', 'Present'],
        datasets: [
          {
            label: 'Candidate 1',
            data: [65, 59, 80, 81, 56, 55, 40],
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
          },
          {
            label: 'Candidate 2',
            data: [40,70,60,67,78,90],
            borderColor: 'rgb(72, 177, 144)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
          },
          {
            label: 'Candidate 3',
            data: [30,50,53,47,36,42],
            borderColor: 'rgb(13, 136, 174)',
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
            display: true,
            text: 'Chart.js Line Chart',
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
