import { zoomies } from 'ldrs'

zoomies.register()

// Default values shown
export default function Loader() {
    return(
        <l-zoomies
        size="80"
        stroke="5"
        bg-opacity="0.1"
        speed="1.4" 
        color="black" 
        ></l-zoomies>
    )
}