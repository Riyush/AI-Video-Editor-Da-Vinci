import React from "react";
import { Box, SimpleGrid } from "@chakra-ui/react";
import PresetCard from "./Preset-Card";

// preset card images
import MinecraftImage from '../../assets/minecraft.jpg';
import FortniteWallpaper from '../../assets/fortnite.jpg';
import AlienWallpaper from '../../assets/alien.jpg';

function DashboardPresetGrid({navigate}) {
    const presets = [
        {
            imageLink : MinecraftImage,
            title : "Basic Edit",
            description : "All the basics to make your footage Youtube Ready",
            cardLabel : "New",
            navigate : navigate,
            page : "basic-edit-page"
        },
        {
            imageLink : FortniteWallpaper,
            title : "Meme Madness",
            description : "add memes and effects for energetic, fast-paced video",
            cardLabel : "Coming Soon",
        },
        {
            imageLink : AlienWallpaper,
            title : "Narrative Editing",
            description : "Create edits that best complement your script",
            cardLabel : "Coming Soon",
        },
        // add more preset cards as needed 
    ];
    return (
        <Box px={8} py = {8}>
            <SimpleGrid columns={3} spacing={4}> 
                {presets.map((preset,index) => (
                    <PresetCard
                    key={index}
                    imageLink={preset.imageLink}
                    title={preset.title}
                    description={preset.description} 
                    cardLabel={preset.cardLabel}
                    navigate = {preset.navigate}
                    page = {preset.page}/>
                ))}
            </SimpleGrid>
        </Box>
    )
}
export default DashboardPresetGrid;