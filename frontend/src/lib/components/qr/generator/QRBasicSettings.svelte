<script lang="ts">
  import ColorPicker from "$lib/components/ui/ColorPicker.svelte";
  import FormGroup from "$lib/components/ui/FormGroup.svelte";
  import FormRow from "$lib/components/ui/FormRow.svelte";
  import SettingsSection from "$lib/components/ui/SettingsSection.svelte";

  interface Props {
    fillColor: string;
    backColor: string;
  }

  let { fillColor = $bindable(), backColor = $bindable() }: Props = $props();
</script>

<SettingsSection h3="Colors">
  <FormRow>
    <FormGroup label="Fill Color" id="fill-color">
      <ColorPicker id="fill-color" bind:value={fillColor} />
    </FormGroup>

    <FormGroup label="Background Color" id="back-color">
      <ColorPicker id="back-color" bind:value={backColor} />
    </FormGroup>
  </FormRow>
</SettingsSection>
