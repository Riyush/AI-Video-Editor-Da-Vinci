import React from "react";
import { Box, SimpleGrid } from "@chakra-ui/react";
import PresetCard from "./Preset-Card";

// preset card images
import MinecraftSwords from '../../assets/minecraft-swords.png';


function DashboardPresetGrid({navigate}) {
    const presets = [
        {
            imageLink : MinecraftSwords,
            title : "Basic Edit",
            description : "All the basics to make your footage Youtube Ready",
            cardLabel : "New",
            navigate : navigate,
            page : "basic-edit-page"
        },
        {
            imageLink : MinecraftSwords,
            title : "Basic Edit",
            description : "All the basics to make your footage Youtube Ready",
            cardLabel : "Coming Soon",
        },
        {
            imageLink : MinecraftSwords,
            title : "Basic Edit",
            description : "All the basics to make your footage Youtube Ready",
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