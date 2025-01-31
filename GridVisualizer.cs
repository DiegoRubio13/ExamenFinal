using UnityEngine;

public class GridVisualizer : MonoBehaviour
{
    public Material goodStreetMaterial;    
    public Material dirtRoadMaterial;      
    public Material crackedStreetMaterial; 
    public Material potholeMaterial;       
    public Material buildingMaterial;      

    public float cellSize = 2f;
    public float buildingHeight = 4f;

    private GameObject gridContainer;

    void Start()
    {
        gridContainer = new GameObject("GridContainer");
        gridContainer.transform.parent = this.transform;
    }

    public void UpdateGrid(int[,] newGrid)
    {
        Debug.Log($"Actualizando grid: {newGrid.GetLength(0)}x{newGrid.GetLength(1)}");

        if (gridContainer != null)
        {
            DestroyImmediate(gridContainer);
        }

        gridContainer = new GameObject("GridContainer");
        gridContainer.transform.parent = this.transform;

        int rows = newGrid.GetLength(0);
        int cols = newGrid.GetLength(1);

        for (int x = 0; x < rows; x++)
        {
            for (int z = 0; z < cols; z++)
            {
        
                GameObject cell = GameObject.CreatePrimitive(PrimitiveType.Cube);
                cell.transform.parent = gridContainer.transform;
                cell.transform.position = new Vector3(z * cellSize, 0, x * cellSize);
                cell.transform.localScale = new Vector3(cellSize * 0.9f, 0.1f, cellSize * 0.9f);

                int gridValue = newGrid[x, z];
                Material material = GetMaterialForGridValue(gridValue);
                cell.GetComponent<Renderer>().material = material;

            
                if (gridValue == -10 || gridValue == -1)
                {
                    GameObject building = GameObject.CreatePrimitive(PrimitiveType.Cube);
                    building.transform.parent = gridContainer.transform;
                    building.transform.position = new Vector3(z * cellSize, buildingHeight / 2, x * cellSize);
                    building.transform.localScale = new Vector3(cellSize * 0.9f, buildingHeight, cellSize * 0.9f);
                    building.GetComponent<Renderer>().material = buildingMaterial;
                }
            }
        }
    }

    Material GetMaterialForGridValue(int value)
    {
        switch (value)
        {
            case 1:
                return goodStreetMaterial;
            case 2:
                return dirtRoadMaterial;
            case 4:
                return crackedStreetMaterial;
            case 5:
                return potholeMaterial;
            case -10:
            case -1:
                return buildingMaterial;
            default:
                Debug.LogWarning($"Valor desconocido en grid: {value}, usando material por defecto");
                return goodStreetMaterial;
        }
    }
}