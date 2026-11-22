import { createTheme } from "@mui/material/styles";

const theme = createTheme({
    palette: {
        mode: "light",

        primary: {
            main: "#5B5DF5",
        },

        secondary: {
            main: "#7C4DFF",
        },

        background: {
            default: "#F5F7FB",
            paper: "#FFFFFF",
        },
    },

    typography: {
        fontFamily: [
            "Inter",
            "Roboto",
            "Helvetica",
            "Arial",
            "sans-serif",
        ].join(","),

        h3: {
            fontWeight: 700,
        },

        h5: {
            fontWeight: 600,
        },

        button: {
            textTransform: "none",
            fontWeight: 600,
        },
    },

    shape: {
        borderRadius: 16,
    },

    components: {
        MuiPaper: {
            styleOverrides: {
                root: {
                    boxShadow: "0 10px 30px rgba(0,0,0,0.06)",
                },
            },
        },

        MuiButton: {
            styleOverrides: {
                root: {
                    borderRadius: 12,
                    padding: "10px 24px",
                },
            },
        },

        MuiTextField: {
            defaultProps: {
                variant: "outlined",
            },
        },
    },
});

export default theme;